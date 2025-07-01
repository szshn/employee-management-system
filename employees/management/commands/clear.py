from django.core.management.base import BaseCommand
from employees.models import Department, Employee

class Command(BaseCommand):
    help = "Clear the database of all data."

    def handle(self, *args, **options):
        self.stdout.write('Clearing database...')
        Employee.objects.all().delete()    # type: ignore
        Department.objects.all().delete()    # type: ignore
        
        self.stdout.write('Cleared database.')