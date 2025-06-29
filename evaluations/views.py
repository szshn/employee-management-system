from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

from .models import Attendance, Performance

# Create your views here.
class AttendanceList(generic.ListView):
    model = Attendance
    
    
class PerformanceList(generic.ListView):
    model = Performance