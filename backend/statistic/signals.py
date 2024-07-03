from users.models import MyUser as User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Statistic

@receiver(post_save, sender=User)
def create_statistic_for_new_user(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        Statistic.objects.create(user=instance)
