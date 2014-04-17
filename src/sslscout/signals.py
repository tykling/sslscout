from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from sslscout.models import Profile

### create profile on user creation
@receiver(post_save, sender=User)
def create_profile(sender, created, instance, **kwargs):
    print "woo signal! %s, %s, %s" % (sender, created, instance)
    if created:
        profile = Profile(user=instance).save()
