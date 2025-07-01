from django.contrib import admin

from .models import Department, Employee

# Register your models here.
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    def manager(self, obj):
        return [x.user.get_full_name() for x in obj.employees.filter(user__is_staff=True)]
    
    def size(self, obj):
        return obj.employees.count()
    
    list_display = ('name', 'manager', 'size')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    def full_address(self, obj):
        return f"{obj.address1}, {obj.address2}, {obj.city}, {obj.state} {obj.zipcode}"

    def location(self, obj):
        return f"{obj.city}, {obj.state}"
    
    def full_name(self, obj):
        return obj.user.get_full_name()
    
    def is_staff_display(self, obj):
        return obj.user.is_staff
    
    is_staff_display.boolean = True
    is_staff_display.short_description = 'Staff Status'
    
    list_display = (
        'full_name',
        'user__email',
        'department',
        'phone',
        'location',
        'is_staff_display'
    )
    list_filter = ('department', 'user__is_staff',)
    search_fields = (
        'user__username',
        'user__first_name',
        'user__last_name'
    )
    ordering = ('user__username',)
