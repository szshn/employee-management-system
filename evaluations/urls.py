from django.urls import path

from . import views

urlpatterns = [
    path("attendances/", views.AttendanceList.as_view(), name="attendance-list"),
    path("attendances/<int:pk>/", views.AttendanceDetail.as_view(), name="attendance-detail"),
    path("performances/", views.PerformanceList.as_view(), name="performance-list"),
    path("performances/<int:pk>/", views.PerformanceDetail.as_view(), name="performance-detail"),
]