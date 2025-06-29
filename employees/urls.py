from django.urls import path

from . import views

urlpatterns = [
    path("", views.api_root),
    path("employees/", views.EmployeeList.as_view(), name="employee-list"),
    path("employees/<int:pk>/", views.EmployeeDetail.as_view(), name="employee-detail"),
    path("departments/", views.DepartmentList.as_view(), name="department-list"),
    path("departments/<int:pk>/", views.DepartmentDetail.as_view(), name="department-detail"),
]