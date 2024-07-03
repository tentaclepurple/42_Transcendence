import os
import base64
import urllib.parse
import requests
from typing import Optional
from requests import Response

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token
from backend.settings import logger
from users.models import MyUser
from users.serializers import CustomRegisterSerializer
from django.http import JsonResponse
from django.shortcuts import redirect
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File
from django.http import HttpResponseRedirect
from uuid import uuid4
from django.db.models.functions import Length

GUEST         = os.environ["DJANGO_GUEST"]
TOKEN_URL     = os.environ["DJANGO_TOKEN_URL"]
AUTH_URL      = os.environ["DJANGO_AUTH_URL"]
LOGIN_URL     = os.environ["DJANGO_LOGIN_URL"]
HOME_URL      = os.environ["DJANGO_HOME_URL"]
#TODO change redirect uri
REDIRECT_URI  = os.environ["DJANGO_REDIRECT_URI"]
CLIENT_ID     = os.environ["DJANGO_CLIENT_ID"]
CLIENT_SECRET = os.environ["DJANGO_CLIENT_SECRET"]
API_42_URL    = os.environ["DJANGO_API_42_URL"]

def generate_state():
    return base64.urlsafe_b64encode(os.urandom(32)).decode('utf-8')

def check_username(username: str) -> bool:
    return MyUser.objects.filter(username=username).exists()

def check_nickname(nickname: str) -> bool:
    return MyUser.objects.filter(nickname=nickname)

def generate_random_nickname() -> str:
    guest_nicknames = MyUser.objects.filter(nickname__regex=r"^guest\d+$").annotate(
        nickname_length=Length('nickname')
    ).order_by('nickname_length', 'nickname')  # god bless GPT

    print(guest_nicknames)
    if not guest_nicknames.exists():
        random_nickname = "guest1"
    else:
        last_guest = guest_nicknames.last().nickname
        guest_count = int(last_guest.strip(GUEST))
        random_nickname = f"{GUEST}{guest_count + 1}"

    return random_nickname

def generate_random_username() -> str:
    guest_usernames = MyUser.objects.filter(username__regex=r"^guest\d+$").annotate(
        username_length=Length('username')
    ).order_by('username_length', 'username')  # god bless GPT

    print(guest_usernames)
    if not guest_usernames.exists():
        random_username = "guest1"
    else:
        last_guest = guest_usernames.last().username
        guest_count = int(last_guest.strip(GUEST))
        random_username = f"{GUEST}{guest_count + 1}"

    return random_username

def register_42user(request, user_info):

    username = user_info.get('login')
    if check_username(username):
        username = generate_random_username()

    nickname = user_info.get('login')
    if check_nickname(nickname):
        nickname = generate_random_nickname()

    email = user_info.get('email')
    avatar = user_info.get('image')
    avatar_url = avatar.get('versions', {}).get('small')

    password = str(uuid4())

    response = requests.get(avatar_url)
    if response.status_code == 200:
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(response.content)
        img_temp.flush()
        img_file = File(img_temp, name=f"{username}_avatar.jpg")
    else:
        img_file = None

    serializer = CustomRegisterSerializer(data={
        'username': username,
        'nickname': nickname,
        'email': email,
        'is_42': True,
        'password1': password,
        'password2': password,
    }, context={'request': request})

    if serializer.is_valid():
        user = serializer.save(request)
        # TODO fix path of photo
        if img_file:
            user.avatar.save(f"{username}_avatar.jpg", img_file)
            user.is_42 = True
            user.save()

        if response.status_code == 200:
            print("Login successful.")
            return user
        else:
            print("Login failed. Status code:", response.status_code)
            return None

    else:
        print(f"Failed to register user. Errors: {serializer.errors}")
    return None

def get_user_info(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}', 
    }
    response = requests.get(API_42_URL, headers=headers)
    return response.json()



def authorize(request):
    
    state = generate_state()
    request.session['oauth_state'] = state 
    scope = 'public'

    params = {
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'response_type': 'code',
        'scope': scope,
        'state': state,
    }

    url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    return redirect(url)

def is_registered(user_info: dict) -> bool:
    return MyUser.objects.filter(email=user_info.get("email"))

def login(username: str, password: str) -> Optional[Response]:

    login_data = {'username': username, 'password': password}

    try:
        response = requests.post(LOGIN_URL, json=login_data, timeout=10)
        return response
    except Exception as ex:
        logger.error(ex)

    return None

def callback(request):
    code = request.GET.get('code') 
    state = request.GET.get('state')

    session_state = request.session.get('oauth_state')

    if state != session_state:
        return JsonResponse({'message': 'Invalid state parameter'}, status=400)

    del request.session['oauth_state']

    try:
        data = {
            'grant_type': 'authorization_code',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code': code,
            'redirect_uri': REDIRECT_URI
        }

        logger.warning(f"Data: {data}")
        response = requests.post(TOKEN_URL, data=data)
        response.raise_for_status()
        token_data = response.json()

        if 'access_token' in token_data:
            access_token = token_data['access_token']
            
            user_info = get_user_info(access_token)
            user = MyUser.objects.filter(email=user_info.get("email")).first()
            if user is None:
                user = register_42user(request, user_info)

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            token_auth, _ = Token.objects.get_or_create(user=user)

            redirect = HttpResponseRedirect(HOME_URL)
            redirect.set_cookie("access_token", access_token)
            redirect.set_cookie("refresh_token", refresh_token)
            redirect.set_cookie("token_auth", token_auth)
            return redirect
        else:
            return JsonResponse({'message': 'Failed to obtain access token'}, status=400)
    
    except requests.exceptions.RequestException as e:
        return JsonResponse({'message': f'Request failed: {str(e)}'}, status=500)
    
    except Exception as e:
        return JsonResponse({'message': f'An error occurred: {str(e)}'}, status=500)