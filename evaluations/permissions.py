from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status

from .models import Employee

def is_in_department(request, department_name):
    if request.user.id is not None:
        try:
            return Employee.objects.get(user=request.user).department.name == department_name  # type: ignore[attr-defined]
        except Employee.DoesNotExist:  # type: ignore[attr-defined]
            return False
    return False

def is_own_record(request, obj):
    if request.user.id is not None:
        try:
            return obj.employee.user == request.user
        except Employee.DoesNotExist:  # type: ignore[attr-defined]
            return False
    return False


class ReportPermissions(permissions.BasePermission):
    """
    Permission class for Attendance and Performance models:
    - Superuser/HR department employees: create/read/update/delete
    - Staff employees: create/read/update for their own department
    - Employees: read for themselves
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if (request.user.is_superuser or
            is_in_department(request, 'HR')):
            return True
            
        if request.user.is_staff and request.method in ['POST', 'PUT', 'PATCH']:
            return True
        
        return False

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        if (request.user.is_superuser or
            is_in_department(request, 'HR')):
            return True
        
        if (request.user.is_staff and
            is_in_department(request, obj.employee.department.name)):
            return True
        
        if (is_own_record(request, obj) and
            request.method in permissions.SAFE_METHODS):
            return True
        
        return False


def get_queryset(request, queryset):
    # Show only active employees
    is_active_param = request.query_params.get('employee__user__is_active')
    if is_active_param is None:
        queryset = queryset.filter(employee__user__is_active=True)
        
    # Check permissions
    if request.user.is_superuser or is_in_department(request, 'HR'):
        return queryset
    
    if request.user.is_staff:
        queryset = queryset.filter(employee__department=request.user.employee.department)
    else:
        queryset = queryset.filter(employee=request.user.employee)
    
    return queryset

def perform_method(request, serializer):
    user = request.user
    employee = serializer.validated_data['employee']
    
    if user.is_superuser or is_in_department(request, 'HR'):
        serializer.save()
    elif user.is_staff:
        if employee.department == user.employee.department:
            serializer.save()
        else:
            raise PermissionDenied(f"You can only {str(request.method)} attendance records for employees in your department.")
    else:
        raise PermissionDenied(f"You do not have permission to {str(request.method)} attendance records.")

def perform_destroy(request, instance):
    if request.user.is_superuser or is_in_department(request, 'HR'):
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        raise PermissionDenied(f"You do not have permission to delete this record.")