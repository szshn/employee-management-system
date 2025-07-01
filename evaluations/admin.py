from django.contrib import admin

from .models import Attendance, Performance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'status')
    list_filter = ('date', 'status')
    search_fields = ('employee__user__first_name', 'employee__user__last_name')
    ordering = ('-date',)

@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'rating', 'review_date')
    list_filter = ('rating', 'review_date')
    search_fields = ('employee__user__first_name', 'employee__user__last_name')
    ordering = ('-review_date',)