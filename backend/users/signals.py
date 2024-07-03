from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from allauth.account.signals import user_signed_up


@receiver(user_logged_out)
def user_logged_out_handler(sender, request, user, **kwargs):
    user.is_connected = False
    user.save()
