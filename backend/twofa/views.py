import os
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from users.models import MyUser
from .models import TwoFaCode
import json
import random
from backend.settings import logger
from django.contrib.auth import authenticate

def twofaform(request):
    return HttpResponse('form ask for twfacode:\n{\n"username":"",\n"email":""\n}')

@csrf_exempt
def send_twofa_email(request):

    try:
        #data = json.loads(request.body.decode('utf-8'))
        #username = data.get('username')
        #password = data.get('password')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if authenticate(username=username, password=password) is None:
            return JsonResponse({'error': 'Wrong username or password.'}, status=404)

        try:
            user = MyUser.objects.get(username=username)
            
            code = random.randint(100000, 999999)

            TwoFaCode.objects.update_or_create(
                user=user,
                defaults={'code': code}
                )
            
            subject = '2fa for Trascendence'
            message = 'Hi ' + username + '. \nThis is your 2FA code: \n' + str(code)
            from_email = os.environ["DJANGO_EMAIL_HOST_USER"]
            recipient_list = [user.email]
    
            send_mail(subject, message, from_email, recipient_list)
    
            return HttpResponse('Email sent.')

        except MyUser.DoesNotExist:
            return JsonResponse({'error': 'User with the provided username and email does not exist.'}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON.'}, status=400)