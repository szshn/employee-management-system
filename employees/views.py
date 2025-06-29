from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

from .models import Employee

# Create your views here.
class IndexView(generic.ListView):
    model = Employee