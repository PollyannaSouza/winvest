from django.urls import path, include
from . import views
from django.shortcuts import redirect
from .views import index_view, chart_data

urlpatterns = [
    path('index/<int:user_id>/', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('', lambda request: redirect('login'), name='home'),
    path('', index_view, name='index'),
    path('chart/data/', chart_data, name='chart_data'),
    path('index/submit_form_compra/<int:user_id>/', views.submit_form_compra, name='submit_form_compra'),
    path('submit_form_venda/<int:user_id>/', views.submit_form_venda, name='submit_form_venda'),
    ]
