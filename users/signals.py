from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Profile

# Creates profile when new user is created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Saves profile when user uodates it
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(user_logged_in)
def create_profile_on_login(sender, request, user, **kwargs):
    if not hasattr(user, 'profile'):
        # Create if it doesn't exist
        Profile.objects.create(user=user)
