
import os

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create the initial deployment superuser if it does not exist"

    def handle(self, *args, **options):
        User = get_user_model()

        username = os.getenv("DJANGO_SUPERUSER_USERNAME")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL", "")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

        if not username or not password:
            self.stdout.write("Superuser environment variables not configured. Skipping.")
            return

        user = User.objects.filter(username=username).first()

        if user:
            if not user.is_superuser:
                raise CommandError(
                    f"Username '{username}' already exists but is not a superuser."
                )

            self.stdout.write("Deployment superuser already exists.")
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )

        self.stdout.write(self.style.SUCCESS("Deployment superuser created!"))
