from django.db import models

from employees.models import Employee

# Create your models here.
class Attendance(models.Model):
    class Status(models.TextChoices):
        PRESENT = 'PRESENT'
        ABSENT = 'ABSENT'
        LATE = 'LATE'
    
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING) # might want to keep old employee's records
    date = models.DateField("Attendance record date")
    status = models.CharField(max_length=7, choices=Status.choices)
    
class Performance(models.Model):
    RATING_CHOICES = [(i,i) for i in range(1,6)]
    
    employee = models.ForeignKey(Employee, on_delete=models.DO_NOTHING)
    rating = models.IntegerField(choices=RATING_CHOICES)
    review_date = models.DateField("Performance review date")
