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
        
        
class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = [
            'id',
            'employee',
            'review_date',
            'rating',
        ]