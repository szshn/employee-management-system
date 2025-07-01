from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name
    
    
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name="employees")
    phone = models.CharField(max_length=10)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=2, help_text="2-character US state code (e.g., 'CA', 'NY')")
    # country = models.CharField(max_length=30)   # if international addresses were to be used
    zipcode = models.CharField(max_length=5)
    
    def __str__(self):
        return self.user.get_full_name()     # type: ignore

    def get_address(self):
        address = f"{self.address1}"
        if self.address2:
            address += f", {self.address2}"
        address += f", {self.city}, {self.state}, {self.zipcode}"
        return address
    
    
    
    
    
    