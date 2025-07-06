from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Create a superuser if none exists'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                username="Sangam",
                email="sangamjangid8@gmail.com",
                password="RoyalStore007"
            )
            self.stdout.write(self.style.SUCCESS("Superuser created successfully."))
        else:
            self.stdout.write(self.style.WARNING("Superuser already exists."))
