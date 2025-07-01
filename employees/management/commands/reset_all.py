from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from employees.models import Employee, Department

class Command(BaseCommand):
    help = "Clear all data including employees, departments, attendance, and performance."

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Skip confirmation prompt'
        )

    def handle(self, *args, **options):
        if not options['force']:
            self.stdout.write(
                self.style.WARNING('This will clear ALL existing data including employees, departments, attendance, and performance. Continue? [y/n]: ')
            )
            response = input().lower().strip()
            if response not in ['y', 'yes']:
                self.stdout.write(self.style.ERROR('Operation cancelled.'))
                return

        self.stdout.write('Clearing all data...')
        
        # Clear evaluations data if the app is installed
        try:
            from evaluations.models import Attendance, Performance
            Attendance.objects.all().delete()
            Performance.objects.all().delete()
            self.stdout.write('Cleared attendance and performance data')
        except ImportError:
            self.stdout.write('Evaluations app not installed - skipping attendance/performance data')
        
        # Clear employee data
        Employee.objects.all().delete()
        Department.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        
        self.stdout.write(
            self.style.SUCCESS('Successfully cleared all data!')
        )
        self.stdout.write(
            self.style.WARNING('Run "python manage.py init_data" to create fresh employee data.')
        )
        self.stdout.write(
            self.style.WARNING('Run "python manage.py init_reports" to create fresh evaluation data (if evaluations app is installed).')
        ) 