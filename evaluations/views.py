from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import Attendance, Performance
from .serializers import AttendanceSerializer, PerformanceSerializer

# Create your views here.
class AttendanceList(generics.ListCreateAPIView):
    queryset = Attendance.objects.all()   # type: ignore
    serializer_class = AttendanceSerializer
    filterset_fields = ['employee', 'date', 'status']
    ordering_fields = ['date', 'status']
    
    def get_queryset(self):
        queryset = Attendance.objects.all()   # type: ignore
        
        is_active_param = self.request.query_params.get('employee__user__is_active')
        if is_active_param is None:
            queryset = queryset.filter(employee__user__is_active=True)
        
        return queryset
    
    # TODO: Add permission classes
    
    
class AttendanceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attendance.objects.all()   # type: ignore
    serializer_class = AttendanceSerializer
    # TODO: Add permission classes
    
    
class PerformanceList(generics.ListCreateAPIView):
    queryset = Performance.objects.all()   # type: ignore
    serializer_class = PerformanceSerializer
    filterset_fields = ['employee', 'review_date', 'rating']
    ordering_fields = ['review_date', 'rating']
    
    def get_queryset(self):
        queryset = Performance.objects.all()   # type: ignore
        
        is_active_param = self.request.query_params.get('employee__user__is_active')
        if is_active_param is None:
            queryset = queryset.filter(employee__user__is_active=True)
        
        return queryset
    
    # TODO: Add permission classes
    
    
class PerformanceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Performance.objects.all()   # type: ignore
    serializer_class = PerformanceSerializer
    # TODO: Add permission classes