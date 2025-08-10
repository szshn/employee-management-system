from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request, format=None):
    return Response({
        "API": {
            'Employees': reverse('employee-list', request=request, format=format),
            'Departments': reverse('department-list', request=request, format=format),
            'Attendances': reverse('attendance-list', request=request, format=format),
            'Performances': reverse('performance-list', request=request, format=format),
        },
        "Login": {
            'Get Token': reverse('token_obtain_pair', request=request, format=format),
            'Refresh Token': reverse('token_refresh', request=request, format=format),
        },
        "Docs": {
            'Swagger': reverse('swagger', request=request, format=format),
            'ReDoc': reverse('redoc', request=request, format=format),
            'Download schema': reverse('schema', request=request, format=format)
        }
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api_root),
    path('', include('employees.urls')),
    path('', include('evaluations.urls')),
    
    # path('api-auth/', include('rest_framework.urls')),    # for session authentication
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),     # for JWT authentication
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),    # for JWT authentication
    
    # drf-spectacular URLs
    path('docs/schema', SpectacularAPIView.as_view(), name='schema'),
    path('docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
    path('docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]   
