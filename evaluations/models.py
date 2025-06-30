from django.db import models
from datetime import date

from employees.models import Employee

# Create your models here.
class Attendance(models.Model):
    class Status(models.TextChoices):
        PRESENT = 'PRESENT'
        ABSENT = 'ABSENT'
        LATE = 'LATE'
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField("Attendance record date", default=date.today())
    status = models.CharField(max_length=7, choices=Status.choices)
    
    def __str__(self):
        return f"{self.employee.first_name} {self.employee.last_name} - Attendance ({self.date})"    # type: ignore
    
class Performance(models.Model):
    RATING_CHOICES = [
        (1, '1 -- Poor'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5 -- Above expectation')
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES, default=5) # type: ignore
    review_date = models.DateField("Performance review date", default=date.today())
    # TODO: Add reviewed by and comment fields
    
    def __str__(self):
        return f"{self.employee.first_name} {self.employee.last_name} - Performance ({self.review_date})"    # type: ignore
