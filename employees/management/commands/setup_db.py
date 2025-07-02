# employees/management/commands/setup_db.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Setup database with superuser'

    def handle(self, *args, **options):
        if not User.objects.filter(is_superuser=True).exists():                    
            User.objects.create_superuser('admin', 'admin@example.com', 'password')
            self.stdout.write(self.style.SUCCESS('Superuser created successfully with username: admin and password: password'))
            self.stdout.write(self.style.WARNING('Please change the password after login'))    
        else:
            self.stdout.write(self.style.SUCCESS('Superuser already exists'))