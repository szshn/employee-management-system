from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Department, Employee
        
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            'id',
            'first_name',
            'last_name',
            'phone',
            'address1',
            'address2',
            'city',
            'state',
            'zipcode',
            'date_of_joining',
            'department',
        ]
        
        
class DepartmentSerializer(serializers.ModelSerializer):
    employees = EmployeeSerializer(many=True, read_only=True)
    
    class Meta:
        model = Department
        fields = [
            'id',
            'name',
            'employees'
        ]