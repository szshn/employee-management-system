from django.db import models
from django.utils import timezone

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name
    
    
class Employee(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=10)     # Assumes 10-digit US phone number only; may update with django-phonenumber-field for ext. or international formats
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=2, help_text="2-character US state code (e.g., 'CA', 'NY')")
    # country = models.CharField(max_length=30)   # if international addresses were to be used
    zipcode = models.CharField(max_length=5)    # Only supports standard 5-digit US ZIP codes; does not support ZIP+4 or international codes
    date_of_joining = models.DateField("Date of joining", default=timezone.now)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, related_name="employees"
    )
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    