from rest_framework import permissions
from rest_framework.views import PermissionDenied
from .models import Employee

def is_in_department(request, department_name):
    if request.user.id is not None:
        try:
            return Employee.objects.get(user=request.user).department.name == department_name  # type: ignore[attr-defined]
        except Employee.DoesNotExist:  # type: ignore[attr-defined]
            return False
    return False


class DepartmentPermissions(permissions.BasePermission):
    """
    Permission class for Department model:
    - Read: Everyone authenticated
    - Create/Update/Delete: HR department employees or superuser
    """
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if (request.method in permissions.SAFE_METHODS or
            request.user.is_superuser or
            is_in_department(request, 'HR')):
            return True
        
        return False


class EmployeePermissions(permissions.BasePermission):
    """
    Permission class for Employee model:
    - Read: Everyone
    - Create/Delete: HR department employees or superuser
    - Update: HR department employees, superuser, or staff employees for their own department
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if (request.method in permissions.SAFE_METHODS or
            request.user.is_superuser or
            is_in_department(request, 'HR') or
            request.user.is_staff):
            return True
        
        return False

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        if (request.method in permissions.SAFE_METHODS or
            request.user.is_superuser or
            is_in_department(request, 'HR')):
            return True
        
        if (request.user.is_staff and
            is_in_department(request, obj.department.name) and
            request.method in ['PUT', 'PATCH']):
            return True
        
        return False
    

def perform_method(request, serializer):
    user = request.user
    department = serializer.validated_data['department']
    
    if user.is_superuser or is_in_department(request, 'HR'):
        serializer.save()
    elif user.is_staff:
        if department == user.department:
            serializer.save()
        else:
            raise PermissionDenied(f"You can only {str(request.method)} employees for employees in your department.")
    else:
        raise PermissionDenied(f"You do not have permission to {str(request.method)} employees.")
