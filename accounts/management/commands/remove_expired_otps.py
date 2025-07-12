from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from accounts.models import OtpCode
from datetime import timedelta

class Command(BaseCommand):
    def handle(self, *args, **options):
        current_time = timezone.now()
        expired_codes = OtpCode.objects.filter(created__lt=current_time+timedelta(minutes=3))
        if expired_codes.exists():
            expired_codes.delete()
            self.stderr.write(self.style.WARNING("expired codes have been removed successfully"))   
        else:
            raise CommandError("No expired code exist !")