from django.db.models.signals import post_save
from .models import User, UserProfile
from django.dispatch import receiver

@receiver(post_save,sender=User)
def create_profile(sender, instance,created,**kwargs):
    try:
        if created:
            UserProfile.objects.create(user=instance).save()
    except Exception as err:
        raise ValueError(f'error creating profile!\n{err}')