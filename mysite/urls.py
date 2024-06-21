from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('DD/',include('Disease_Diagnosis.urls')),
    path('auth/',include('djoser.urls')),
    path('auth/',include('djoser.urls.authtoken')),
    path('Token/login', views.obtain_auth_token),
    # path('token/logout', views.obtain_auth_token),
]

