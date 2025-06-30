from django.views import generic
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination

from .models import Employee, Department
from .serializers import EmployeeSerializer, DepartmentSerializer

# Create your views here.
class SingleResultPagination(LimitOffsetPagination):
    default_limit = 1
    

class EmployeeList(generics.ListCreateAPIView):
    queryset = Employee.objects.all()   # type: ignore
    serializer_class = EmployeeSerializer
    # TODO: Add permission classes
    
    
class EmployeeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()   # type: ignore
    serializer_class = EmployeeSerializer
    # TODO: Add permission classes
    
    
class DepartmentList(generics.ListCreateAPIView):
    queryset = Department.objects.all()   # type: ignore
    serializer_class = DepartmentSerializer
    pagination_class = SingleResultPagination
    # TODO: Add permission classes
    
    
class DepartmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()   # type: ignore    
    serializer_class = DepartmentSerializer
    # TODO: Add permission classes