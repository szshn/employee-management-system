import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from employees.models import Employee
from evaluations.models import Attendance, Performance

class Command(BaseCommand):
    help = "Initialize attendance and performance data for employees."

    def add_arguments(self, parser):
        parser.add_argument(
            '--attendance',
            type=int,
            default=20,
            help='Number of attendance records to create (default: 20)'
        )
        parser.add_argument(
            '--reviews',
            type=int,
            default=10,
            help='Number of performance reviews to create (default: 10)'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Skip confirmation prompt'
        )

    def handle(self, *args, **options):
        if not options['force'] and (Attendance.objects.exists() or Performance.objects.exists()):
            self.stdout.write(
                self.style.WARNING('This will clear all existing attendance and performance data. Continue? [y/n]: ')
            )
            response = input().lower().strip()
            if response not in ['y', 'yes']:
                self.stdout.write(self.style.ERROR('Operation cancelled.'))
                return

        self.stdout.write('Clearing existing attendance and performance data...')
        Attendance.objects.all().delete()    # type: ignore
        Performance.objects.all().delete()    # type: ignore
        
        today = timezone.now().date()
        attendance_count = options['attendance']
        reviews_count = options['reviews']
        
        # Get all active employees
        employees = Employee.objects.filter(user__is_active=True)    # type: ignore
        
        if not employees.exists():
            self.stdout.write(
                self.style.ERROR('No active employees found. Please run init_data first.')
            )
            return
        
        self.stdout.write(f'Creating {attendance_count} attendance records...')
        attendance_records = []
        
        # Create specified number of attendance records
        for _ in range(attendance_count):
            # Try to find a valid employee/date combination
            max_attempts = 5  # Prevent infinite loops
            attempts = 0
            record_created = False
            
            while attempts < max_attempts and not record_created:
                # Randomly select an employee
                employee = random.choice(employees)
                employee_joined = employee.user.date_joined.date()
                
                # Generate a random date between employee's join date and today (inclusive)
                if employee_joined < today:
                    days_since_joined = (today - employee_joined).days
                    random_days = random.randint(0, days_since_joined)
                    attendance_date = employee_joined + timedelta(days=random_days)
                else:
                    # Employee joined today, use today
                    attendance_date = today
                
                # Check if attendance already exists for this date/employee
                if not Attendance.objects.filter(employee=employee, date=attendance_date).exists():
                    attendance_records.append(Attendance(
                        employee=employee,
                        date=attendance_date,
                        status=random.choice([Attendance.Status.PRESENT, Attendance.Status.LATE, Attendance.Status.ABSENT])
                    ))
                    record_created = True
                else:
                    attempts += 1
            
            if not record_created:
                self.stdout.write(f'Could not find unique combination for attendance record after {max_attempts} attempts')
        
        # Bulk create attendance records
        if attendance_records:
            Attendance.objects.bulk_create(attendance_records)    # type: ignore
            self.stdout.write(f'Created {len(attendance_records)} attendance records')
        else:
            self.stdout.write('No attendance records could be created')
        
        self.stdout.write(f'Creating {reviews_count} performance reviews...')
        performance_records = []
        
        # Create specified number of performance reviews
        for _ in range(reviews_count):
            # Try to find a valid employee/date combination
            max_attempts = 100  # Prevent infinite loops
            attempts = 0
            record_created = False
            
            while attempts < max_attempts and not record_created:
                # Randomly select an employee
                employee = random.choice(employees)
                employee_joined = employee.user.date_joined.date()
                
                # Generate a review date between employee's join date and today
                if employee_joined < today:
                    days_since_joined = (today - employee_joined).days
                    random_days = random.randint(0, days_since_joined)
                    review_date = employee_joined + timedelta(days=random_days)
                else:
                    review_date = today
                
                # Check if performance review already exists for this date/employee
                if not Performance.objects.filter(employee=employee, review_date=review_date).exists():
                    performance_records.append(Performance(
                        employee=employee,
                        rating=random.randint(1, 5),
                        review_date=review_date
                    ))
                    record_created = True
                else:
                    attempts += 1
            
            if not record_created:
                self.stdout.write(f'Could not find unique combination for performance review after {max_attempts} attempts')
        
        # Bulk create performance records
        if performance_records:
            Performance.objects.bulk_create(performance_records)    # type: ignore
            self.stdout.write(f'Created {len(performance_records)} performance reviews')
        else:
            self.stdout.write('No performance reviews could be created')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {len(attendance_records)} attendance records and {len(performance_records)} performance reviews!')  # type: ignore
        )