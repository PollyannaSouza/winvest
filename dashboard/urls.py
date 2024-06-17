from django.urls import path, include
from . import views

urlpatterns = [
    path('index/<int:user_id>/', views.index, name='index'),
    path('login/', views.login_view, name='login')
]