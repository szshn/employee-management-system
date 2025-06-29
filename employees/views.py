from django.views import generic
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import Employee, Department
from .serializers import EmployeeSerializer, DepartmentSerializer

# Create your views here.
@api_view(['GET'])
def api_root(request, format=None):
    return Response(
        {
            'Employees': reverse('employee-list', request=request, format=format),
            'Departments': reverse('department-list', request=request, format=format),
        }
    )

class EmployeeList(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    
    
class EmployeeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    

class DepartmentList(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    
    
class DepartmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer