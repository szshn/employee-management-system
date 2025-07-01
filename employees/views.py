from django.views import generic
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from django_filters import FilterSet

from .models import Employee, Department
from .serializers import EmployeeSerializer, DepartmentSerializer
from .permissions import EmployeePermissions, DepartmentPermissions, perform_method

# Create your views here.
class SingleResultPagination(LimitOffsetPagination):
    default_limit = 1
    
class EmployeeFilter(FilterSet):
    class Meta:
        model = Employee
        fields = ['department', 'user__first_name', 'user__last_name', 'city', 'state', 'user__is_active']

class EmployeeList(generics.ListCreateAPIView):
    queryset = Employee.objects.all()   # type: ignore
    serializer_class = EmployeeSerializer
    filterset_class = EmployeeFilter
    ordering_fields = ['department', 'user__first_name', 'user__last_name', 'user__date_joined']
    permission_classes = [EmployeePermissions]
    
    def get_queryset(self):
        queryset = Employee.objects.all()   # type: ignore
        
        is_active_param = self.request.query_params.get('user__is_active')
        if is_active_param is None:
            queryset = queryset.filter(user__is_active=True)
        
        return queryset
    
    
class EmployeeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()   # type: ignore
    serializer_class = EmployeeSerializer
    permission_classes = [EmployeePermissions]
    
    def perform_update(self, serializer):
        return perform_method(self.request, serializer)
    
    
class DepartmentList(generics.ListCreateAPIView):
    queryset = Department.objects.all()   # type: ignore
    serializer_class = DepartmentSerializer
    pagination_class = SingleResultPagination
    filterset_fields = ['name']
    ordering_fields = ['name']
    permission_classes = [DepartmentPermissions]
    
    def get_queryset(self):
        queryset = Department.objects.all()   # type: ignore
        
        is_active_param = self.request.query_params.get('user__is_active')
        if is_active_param is None:
            queryset = queryset.filter(employees__user__is_active=True).distinct()
        
        return queryset
    
    
class DepartmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()   # type: ignore    
    serializer_class = DepartmentSerializer
    permission_classes = [DepartmentPermissions]