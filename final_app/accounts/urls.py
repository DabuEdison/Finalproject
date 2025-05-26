from django.urls import path
from . import views  # Make sure to import views from the current app
from .api_views import RegisterView, ProfileView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # API paths
    path('api/register/', RegisterView.as_view(), name='api-register'),
    path('api/me/', ProfileView.as_view(), name='api-profile'),
    path('api/token/', TokenObtainPairView.as_view(), name='token-obtain'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    
    
    # Template rendering paths
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
]
