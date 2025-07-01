from rest_framework import serializers
from .models import Attendance, Performance
        
class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = [
            'id',
            'employee',
            'date',
            'status',
        ]
        
    def validate_employee(self, value):
        if not value.user.is_active:
            raise serializers.ValidationError("Cannot create attendance for inactive employee.")
        return value
        
        
class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = [
            'id',
            'employee',
            'review_date',
            'rating',
        ]
        
    def validate_employee(self, value):
        if not value.user.is_active:
            raise serializers.ValidationError("Cannot create performance for inactive employee.")
        return value