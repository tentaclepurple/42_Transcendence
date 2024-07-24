#oauth/views.py

import os
import base64
import urllib.parse
import json
from django.shortcuts import redirect
import requests
from users.serializers import CustomRegisterSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, authentication_classes, permission_classes




def generate_state():
    return base64.urlsafe_b64encode(os.urandom(32)).decode('utf-8')




def register_42user(request, user_info):

    username = user_info.get('login')
    email = user_info.get('email')
    avatar = user_info.get('image')

    avatar_url = avatar.get('versions', {}).get('small')

    print("AVATAR: ", avatar_url)

    password = generate_state()

    serializer = CustomRegisterSerializer(data={
        'username': username,
        'email': email,
        'is_42': True,
        'password1': password,
        'password2': password,
        #'avatar': avatar_url
    }, context={'request': request})
    
    if serializer.is_valid():
        user = serializer.save(request)
        login_url = 'http://localhost:8000/auth/login/'
        login_data = {'username': username, 'code': '11111', 'password': password}

        response = requests.post(login_url, json=login_data)

        if response.status_code == 200:
            print("Login successful.")
        else:
            print("Login failed. Status code:", response.status_code)

    else:
        print(f"Failed to register user. Errors: {serializer.errors}")

    


@csrf_exempt
@permission_classes([AllowAny])
def get_user_info(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}', 
    }
    response = requests.get('https://api.intra.42.fr/v2/me', headers=headers)
    return response.json()

""" @csrf_exempt
@permission_classes([AllowAny])
def get_campuses(access_token):
    
    headers = {
        'Authorization': f'Bearer {access_token}', 
    }
    campus_url = 'https://api.intra.42.fr/v2/users?campus_id=40&sort=-updated_at&page[size]=100'

    response = requests.get(campus_url, headers=headers)
    response.raise_for_status()  # Lanza una excepción para errores HTTP

    campuses = response.json()
    
    file_path = os.path.join('api', 'users.json')  # Ajusta el path a tu directorio preferido
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(campuses, file, ensure_ascii=False, indent=4)
    
    
    #return JsonResponse(campuses, status=200) """


@csrf_exempt
@permission_classes([AllowAny])
def get_campuses(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    base_url = 'https://api.intra.42.fr/v2/users?campus_id=40&sort=-updated_at&page[size]=100&&range[level]=0.0,30'
    
    page_number = 0
    all_users = []

    while True:
        campus_url = f"{base_url}&page[number]={page_number}"
        
        response = requests.get(campus_url, headers=headers)
        response.raise_for_status()
        
        users = response.json()
        
        if not users:
            break
        
        all_users.extend(users)
        page_number += 1

    file_path = os.path.join('api', 'users.json')
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(all_users, file, ensure_ascii=False, indent=4)


    print("---------------FINISHED---------")

    return JsonResponse(all_users, safe=False, status=200)






@permission_classes([AllowAny])
def authorize(request):
    
    client_id = 'u-s4t2ud-ca8799da64518f941f7a66f9693a5c426aa78da783ba9eec6cf79dee9740221b'
    redirect_uri = 'http://localhost:8000/oauth/callback'
    state = generate_state()
    request.session['oauth_state'] = state 
    scope = 'public'

    auth_url = 'https://api.intra.42.fr/oauth/authorize'
    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'scope': scope,
        'state': state,
    }

    url = f"{auth_url}?{urllib.parse.urlencode(params)}"
    return redirect(url)





@csrf_exempt
def callback(request):
    code = request.GET.get('code') 
    state = request.GET.get('state')

    session_state = request.session.get('oauth_state')

    if state != session_state:
        return JsonResponse({'message': 'Invalid state parameter'}, status=400)

    del request.session['oauth_state']

    try:
        token_url = 'https://api.intra.42.fr/oauth/token'
        
        data = {
            'grant_type': 'authorization_code',
            'client_id': 'u-s4t2ud-ca8799da64518f941f7a66f9693a5c426aa78da783ba9eec6cf79dee9740221b',
            'client_secret': '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',
            'code': code,
            'redirect_uri': 'http://localhost:8000/oauth/callback',
        }

        response = requests.post(token_url, data=data)
        response.raise_for_status()
        token_data = response.json()



        if 'access_token' in token_data:
            access_token = token_data['access_token']
            
            print("-----", access_token)

            get_campuses(access_token)

            #user_info = get_user_info(access_token)
            
            #register_42user(request, user_info)

            return JsonResponse({'message': 'User registered successfully.'}, status=200)
        else:
            return JsonResponse({'message': 'Failed to obtain access token'}, status=400)
    
    except requests.exceptions.RequestException as e:
        return JsonResponse({'message': f'Request failed: {str(e)}'}, status=500)
    
    except Exception as e:
        return JsonResponse({'message': f'An error occurred: {str(e)}'}, status=500)