from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from users.models import MyUser
from .models import TwoFaCode
import json
import random

def twofaform(request):
    return HttpResponse('form ask for twfacode:\n{\n"username":"",\n"email":""\n}')


@csrf_exempt
def send_twofa_email(request):
    
    try:
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        email = data.get('email')

        try:
            user = MyUser.objects.get(username=username, email=email)
            
            code = random.randint(0, 999999)

            TwoFaCode.objects.update_or_create(
                user=user,
                defaults={'code': code}
                )
            
            subject = '2fa for Trascendence'
            message = 'Hi ' + username + '. \nThis is your 2FA code: \n' + str(code)
            from_email = '42trascendence@gmail.com'
            recipient_list = [email]
    
            send_mail(subject, message, from_email, recipient_list)
    
            return HttpResponse('Email sent.')

        except MyUser.DoesNotExist:
            return JsonResponse({'error': 'User with the provided username and email does not exist.'}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON.'}, status=400)

    

    

