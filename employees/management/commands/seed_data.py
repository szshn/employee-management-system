from django.core.management.base import BaseCommand, CommandError
from employees.models import Department, Employee
from datetime import date
from faker import Faker
import random

class Command(BaseCommand):
    help = "Seed the database with initial data. Clears if any existing data is present."

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

    def handle(self, *args, **options):
        self.stdout.write('Clearing existing employee data...')
        Employee.objects.all().delete()    # type: ignore
        
        random.seed(options['seed'])
        Faker.seed(options['seed'])
        
        fake = Faker()
        count = options['count']
        
        self.stdout.write('Creating departments...')
        departments = []
        dept_names = ['HR', 'Engineering', 'Sales', 'Marketing', 'Finance', 'Operations', 'IT', 'Customer Support']
        
        for dept_name in dept_names:
            dept, created = Department.objects.get_or_create(name=dept_name)    # type: ignore
            departments.append(dept)
            if created:
                self.stdout.write(f'Created department: {dept_name}')
        
        self.stdout.write('Creating employees...')
        
        for i in range(count):
            Employee.objects.create(    # type: ignore
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone=fake.numerify(text='##########'),
                address1=fake.street_address(),
                address2=fake.secondary_address() if random.choice([True, False]) else None,
                city=fake.city(),
                state=fake.state_abbr(),
                zipcode=fake.numerify(text='#####'),
                date_of_joining=fake.date_between(start_date='-1y', end_date='today'),
                department=random.choice(departments),
            )
            
            if (i + 1) % 10 == 0:
                self.stdout.write(f'Created {i+1} employees...')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {count} employees and {len(departments)} departments!')    # type: ignore
        )