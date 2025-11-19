from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Creates a fake user to be used to login with a passphrase'

    def handle(self, *args, **options):
        User.objects.create_user(username=settings.AUTHENTICATED_VISITOR_USERNAME,
                                 email=settings.AUTHENTICATED_VISITOR_USERNAME,
                                 password=settings.AUTHENTICATED_VISITOR_PASSWORD)

        self.stdout.write(self.style.SUCCESS('User successfully created!'))