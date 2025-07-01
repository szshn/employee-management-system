import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from employees.models import Department, Employee
from faker import Faker

class Command(BaseCommand):
    help = "Add more employees without clearing existing data."

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of additional employees to create (default: 10)'
        )
        parser.add_argument(
            '--seed',
            type=int,
            default=1,
            help='Seed for reproducible fake data (default: 1)'
        )

    def handle(self, *args, **options):
        # Check if departments exist
        if not Department.objects.exists():
            self.stdout.write(
                self.style.ERROR('Empty dataset: please run init_data first.')
            )
            return

        seed = options['seed']
        
        # Check for duplicate seed usage by creating a test user with the same seed
        Faker.seed(options['seed'])
        test_faker = Faker()
        test_first_name = test_faker.first_name()
        test_last_name = test_faker.last_name()
        test_username = f"{test_first_name.lower()}{test_last_name[0].lower()}"
        
        # Check if this exact username already exists
        if User.objects.filter(username=test_username).exists():
            self.stdout.write(
                self.style.WARNING(f'Warning: Seed {seed} has been used before. This will create duplicate data.')
            )
            while True:
                new_seed = input('Please provide a different seed: ').strip()
                try:
                    new_seed = int(new_seed)
                    # Test the new seed
                    Faker.seed(new_seed)
                    test_faker = Faker()
                    test_first_name = test_faker.first_name()
                    test_last_name = test_faker.last_name()
                    test_username = f"{test_first_name.lower()}{test_last_name[0].lower()}"
                    
                    if not User.objects.filter(username=test_username).exists():
                        seed = new_seed
                        break
                    else:
                        self.stdout.write(
                            self.style.WARNING(f'Seed {new_seed} also creates duplicate data. Please try another seed.')
                        )
                except ValueError:
                    self.stdout.write(
                        self.style.ERROR('Please enter a valid integer for the seed.')
                    )

        random.seed(seed)
        Faker.seed(options['seed'])
        
        fake = Faker()
        count = options['count']
        
        self.stdout.write(f'Adding {count} more employees...')
        
        departments = list(Department.objects.all())
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
            
            if (i + 1) % 5 == 0:
                self.stdout.write(f'Created {i+1} additional employees...')

        User.objects.bulk_create(users_to_create)
        Employee.objects.bulk_create(employees_to_create)
            
        self.stdout.write(
            self.style.SUCCESS(f'Successfully added {count} more employees!')
        ) 