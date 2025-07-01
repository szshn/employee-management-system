import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from employees.models import Employee
from evaluations.models import Attendance, Performance

class Command(BaseCommand):
    help = "Add more attendance and performance data without clearing existing data."

    def add_arguments(self, parser):
        parser.add_argument(
            '--attendance',
            type=int,
            default=5,
            help='Number of additional attendance records to create (default: 5)'
        )
        parser.add_argument(
            '--reviews',
            type=int,
            default=5,
            help='Number of additional performance reviews to create (default: 5)'
        )

    def handle(self, *args, **options):
        # Check if employees exist
        if not Employee.objects.exists():
            self.stdout.write(
                self.style.ERROR('Empty dataset: please run init_reports first.')
            )
            return

        today = timezone.now().date()
        attendance_count = options['attendance']
        reviews = options['reviews']
        
        # Get all active employees
        employees = Employee.objects.filter(user__is_active=True)
        
        self.stdout.write(f'Adding {attendance_count} attendance records...')
        attendance_records = []
        
        # Create specified number of attendance records
        for _ in range(attendance_count):
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
        
        # Bulk create attendance records
        if len(attendance_records) == attendance_count:
            Attendance.objects.bulk_create(attendance_records)
            self.stdout.write(f'Created {len(attendance_records)} attendance records')
        elif attendance_count == 0:
            self.stdout.write('No new attendance records could be created')
        else:
            self.stdout.write(f'Only {len(attendance_records)} attendance records could be created')
        
        self.stdout.write(f'Adding {reviews} performance reviews...')
        performance_records = []
        
        # Create specified number of performance reviews
        for _ in range(reviews):
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
            
            performance_records.append(Performance(
                employee=employee,
                rating=random.randint(1, 5),
                review_date=review_date
            ))
        
        # Bulk create performance records
        if len(performance_records) == reviews:
            Performance.objects.bulk_create(performance_records)
            self.stdout.write(f'Created {len(performance_records)} performance reviews')
        elif reviews == 0:
            self.stdout.write('No new performance reviews needed')
        else:
            self.stdout.write(f'Only {len(performance_records)} performance reviews could be created')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully added attendance and performance data!')
        ) 