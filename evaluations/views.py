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
    # TODO: Add permission classes
    
class AttendanceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attendance.objects.all()   # type: ignore
    serializer_class = AttendanceSerializer
    # TODO: Add permission classes
    
class PerformanceList(generics.ListCreateAPIView):
    queryset = Performance.objects.all()   # type: ignore
    serializer_class = PerformanceSerializer
    # TODO: Add permission classes
    
class PerformanceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Performance.objects.all()   # type: ignore
    serializer_class = PerformanceSerializer
    # TODO: Add permission classes