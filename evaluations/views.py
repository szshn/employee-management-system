from rest_framework import generics
from rest_framework import permissions

from .models import Attendance, Performance
from .serializers import AttendanceSerializer, PerformanceSerializer
from .permissions import ReportPermissions, get_queryset, perform_method, perform_destroy

# Create your views here.
class AttendanceList(generics.ListCreateAPIView):
    queryset = Attendance.objects.all()   # type: ignore
    serializer_class = AttendanceSerializer
    filterset_fields = ['employee', 'date', 'status']
    ordering_fields = ['date', 'status']
    permission_classes = [ReportPermissions]
    
    def get_queryset(self):
        return get_queryset(self.request, self.queryset)
    
    def perform_create(self, serializer):
        return perform_method(self.request, serializer)
    
class AttendanceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attendance.objects.all()   # type: ignore
    serializer_class = AttendanceSerializer
    permission_classes = [ReportPermissions]
    
    def perform_update(self, serializer):
        return perform_method(self.request, serializer)
    
    def perform_destroy(self, request, *args, **kwargs):
        return perform_destroy(self.request, self.get_object())
    
class PerformanceList(generics.ListCreateAPIView):
    queryset = Performance.objects.all()   # type: ignore
    serializer_class = PerformanceSerializer
    filterset_fields = ['employee', 'review_date', 'rating']
    ordering_fields = ['review_date', 'rating']
    permission_classes = [ReportPermissions]
    
    def get_queryset(self):
        return get_queryset(self.request, self.queryset)
    
    def perform_create(self, serializer):
        return perform_method(self.request, serializer)
    
    
class PerformanceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Performance.objects.all()   # type: ignore
    serializer_class = PerformanceSerializer
    permission_classes = [ReportPermissions]
    
    def perform_update(self, serializer):
        return perform_method(self.request, serializer)
    
    def perform_destroy(self, request, *args, **kwargs):
        return perform_destroy(self.request, self.get_object())