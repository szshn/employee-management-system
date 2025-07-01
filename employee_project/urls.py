from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

@api_view(['GET'])
def api_root(request, format=None):
    return Response(
        {
            'Employees': reverse('employee-list', request=request, format=format),
            'Departments': reverse('department-list', request=request, format=format),
            'Attendances': reverse('attendance-list', request=request, format=format),
            'Performances': reverse('performance-list', request=request, format=format),
        }
    )


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api_root),
    path('', include('employees.urls')),
    path('', include('evaluations.urls')),
    
    # path('api-auth/', include('rest_framework.urls')),    # for session authentication
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),     # for JWT authentication
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),    # for JWT authentication
    
    # drf-spectacular URLs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]   
