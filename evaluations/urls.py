from django.urls import path

from . import views

urlpatterns = [
    path("attendance/", views.AttendanceList.as_view(), name="attendance-index"),
    path("performance/", views.PerformanceList.as_view(), name="performance-index"),
]