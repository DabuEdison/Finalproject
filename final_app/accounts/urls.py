from django.urls import path
from . import views  
from .api_views import RegisterView, ProfileView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from .api_views import BlogPostViewSet, GoalViewSet, CommentViewSet
from django.urls import include


router = DefaultRouter()
router.register(r'posts', BlogPostViewSet, basename='posts')
router.register(r'goals', GoalViewSet, basename='goals')
router.register(r'comments', CommentViewSet, basename='comments')

urlpatterns = [

    # API paths
    path('api/register/', RegisterView.as_view(), name='api-register'),
    path('api/me/', ProfileView.as_view(), name='api-profile'),
    path('api/token/', TokenObtainPairView.as_view(), name='token-obtain'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('api/', include(router.urls)),
    
    # Template rendering paths
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('posts/', views.posts_view, name='posts'),
    path('goals/', views.goals_view, name='goals'),
]
