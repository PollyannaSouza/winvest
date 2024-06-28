from django.urls import path, include
from . import views
from django.shortcuts import redirect

urlpatterns = [
    path('index/<int:user_id>/', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('', lambda request: redirect('login'), name='home'),
]