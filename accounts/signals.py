import logging

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import UserProfiles


logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def create_usersettings_on_user_create(sender, **kwargs):
    """
    Automatically create a UserProfiles object when a new user is created.
    """
    instance = kwargs['instance']

    if kwargs.get('created', True):
        UserProfiles.objects.get_or_create(user=instance)