from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Farmer

@receiver(post_save, sender=User)
def create_farmer(sender, instance, created, **kwargs):
    if created:
        print("==== new user created =====")
        Farmer.objects.create(user=instance,name=instance.first_name+" "+instance.last_name,email=instance.email)


@receiver(post_save, sender=User)
def save_farmer(sender, instance, **kwargs):
    print("==== new user saved =====")
    instance.farmer.save()