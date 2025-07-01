import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from employees.models import Department, Employee
from faker import Faker

class Command(BaseCommand):
    help = "Complete initialization - clears everything and creates fresh employee data."

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=40,
            help='Number of employees to create (default: 40)'
        )
        parser.add_argument(
            '--seed',
            type=int,
            default=0,
            help='Seed for reproducible fake data (default: 0)'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Skip confirmation prompt'
        )

    def handle(self, *args, **options):
        if not options['force'] and Employee.objects.exists():
            self.stdout.write(
                self.style.WARNING('This will clear all existing employee data. Continue? [y/n]: ')
            )
            response = input().lower().strip()
            if response not in ['y', 'yes']:
                self.stdout.write(self.style.ERROR('Operation cancelled.'))
                return

        self.stdout.write('Clearing existing employee data...')
        Employee.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        
        random.seed(options['seed'])
        Faker.seed(options['seed'])
        
        fake = Faker()
        count = options['count']
        
        self.stdout.write('Creating departments...')
        departments = []
        dept_names = ['HR', 'Engineering', 'Sales', 'Marketing', 'Finance', 'Operations', 'IT', 'Customer Support']
        
        for dept_name in dept_names:
            dept, created = Department.objects.get_or_create(name=dept_name)
            departments.append(dept)
            if created:
                self.stdout.write(f'Created department: {dept_name}')
        
        self.stdout.write('Creating employees...')

        users_to_create = []
        employees_to_create = []

        for i in range(count):
            first_name, last_name = fake.first_name(), fake.last_name()
            username = f"{first_name.lower()}{last_name[0].lower()}"
            
            counter = 2
            original_username = username
            while User.objects.filter(username=username).exists():
                username = f"{original_username}{counter}"
                counter += 1
            
            date_joined = fake.date_between(start_date='-1y', end_date='today')
            date_joined = timezone.make_aware(
                timezone.datetime.combine(date_joined, timezone.datetime.min.time())
            )
            
            user = User(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=f"{username}@example.com",
                password='password123',
                date_joined=date_joined,
            )
            employee = Employee(
                user=user,
                department=random.choice(departments),
                phone=fake.numerify(text='(###) ###-####'),
                address1=fake.street_address(),
                address2=fake.secondary_address() if random.choice([True, False]) else None,
                city=fake.city(),
                state=fake.state_abbr(),
                zipcode=fake.numerify(text='#####'),
            )
            
            users_to_create.append(user)
            employees_to_create.append(employee)
            
            if employee.department.name == 'HR':
                employee.user.is_staff = True
            
            if (i + 1) % 10 == 0:
                self.stdout.write(f'Created {i+1} employees...')

        User.objects.bulk_create(users_to_create)
        Employee.objects.bulk_create(employees_to_create)
        
        self.stdout.write('Creating managers...')
        
        managers = []
        for dept in departments:
            if dept.name == 'HR':
                continue
            
            dept.manager = random.choice(Employee.objects.filter(department=dept))
            dept.manager.user.is_staff = True
            managers.append(dept.manager.user)
            
        User.objects.bulk_update(managers, ['is_staff'])
            
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {count} employees and {len(departments)} departments!')
        )
        self.stdout.write(
            self.style.WARNING('Run "python manage.py init_reports" to create evaluation data (if evaluations app is installed).')
        ) 