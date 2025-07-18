"""magnetlinks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('login/', views.sign_in, name='login'),
    #path('logout/', views.sign_out, name='logout'),
    path('register/', views.sign_up, name='register'),
    path('newmagnetlink/', views.new_magnetlink, name='newmagnetlink'),
    path('magnetlink/<int:id>/', views.magnetlink_detail, name='magnetlink_detail'),
    path('captcha/', include('captcha.urls')),
    path('', RedirectView.as_view(url='/home/', permanent=False))  # <-- Redirección
]
    
