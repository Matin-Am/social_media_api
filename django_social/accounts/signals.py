from django.conf import settings
from django.db.models import signals
from django.contrib.auth.signals import user_logged_in
from rest_framework.authtoken.models import Token
from django.dispatch import receiver



@receiver(signal=signals.post_save,sender = settings.AUTH_USER_MODEL)
def create_token(sender,instance=None,created=False,**kwargs):
    if created:
        Token.objects.create(user=instance)