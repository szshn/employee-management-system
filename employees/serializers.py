from rest_framework import serializers
from .models import Department, Employee
        
class EmployeeSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    date_joined = serializers.DateTimeField(source='user.date_joined')
    is_staff = serializers.BooleanField(source='user.is_staff')
    is_active = serializers.BooleanField(source='user.is_active')
    
    class Meta:
        model = Employee
        fields = [
            'id',
            'first_name',
            'last_name',
            'department',
            'phone',
            'is_staff',
            'is_active',
            'date_joined',
            'address1',
            'address2',
            'city',
            'state',
            'zipcode'
        ]
        
        
class DepartmentSerializer(serializers.ModelSerializer):
    employees = serializers.SerializerMethodField()
    
    def get_employees(self, obj):
        return [
            {
                'id': employee.id,
                'full_name': employee.user.get_full_name(),
                'email': employee.user.email
            }
            for employee in obj.employees.all()
        ]
    
    class Meta:
        model = Department
        fields = [
            'id',
            'name',
            'employees'
        ]