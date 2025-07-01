from rest_framework import permissions
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
    - Delete: Superuser only
    - Create/Update: HR department employees or superuser
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
    - Delete: Superuser only
    - Create: HR department employees or superuser
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