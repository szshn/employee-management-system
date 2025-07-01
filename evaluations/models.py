from django.db import models
from django.utils import timezone

from employees.models import Employee

# Create your models here.
class Attendance(models.Model):
    class Status(models.TextChoices):
        PRESENT = 'PRESENT'
        ABSENT = 'ABSENT'
        LATE = 'LATE'
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=False)
    date = models.DateField("Attendance record date", default=timezone.now)
    status = models.CharField(max_length=7, choices=Status.choices)
    
    def __str__(self):
        return f"{self.employee.get_full_name()} - Attendance ({self.date})"    # type: ignore
    
class Performance(models.Model):
    RATING_CHOICES = [
        (1, '1 -- Poor'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5 -- Above expectation')
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=False)
    rating = models.IntegerField(choices=RATING_CHOICES, default=5) # type: ignore
    review_date = models.DateField("Performance review date", default=timezone.now)
    # TODO: Add reviewed by and comment fields
    
    def __str__(self):
        return f"{self.employee.get_full_name()} - Performance ({self.review_date})"    # type: ignore
