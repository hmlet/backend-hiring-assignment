"""hmlet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# from django.urls import path
from django.contrib.auth import views as auth_views
from users import views as user_views 
from django.urls import path,include
from django.conf import settings
from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


from photos import views

from django.views.generic import RedirectView

urlpatterns = [
    #URL FOR ADMIN LOGIN
    path('admin/', admin.site.urls),

    #URL FOR NEW REGISTER
    path('register/', user_views.register,name ='register'),

    #URL FOR USER'S PROFILE
    path('profile/', user_views.profile,name ='profile'),

    #URL FOR NEW LOGIN
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'),name ='login'),

    #URL FOR LOGOUT
    path('logout', auth_views.LogoutView.as_view(template_name='users/logout.html'),name ='logout'),

    #URL FOR ALL PHOTOS
    path('photos/', include('photos.urls')),

    #URL FOR JWT TOKEN AND TOKEN REFRESH
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    path('', views.blog_view, name='blog'),
    path('<int:id>/', views.detail_view, name='detail'),    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)