from django.shortcuts import render, redirect
from django.urls import reverse
from dashboard.src.login import login_user
from django.http import JsonResponse

import random

from dashboard.src.user import get_total_por_ticker,get_noticias, nome_user

def index(request, user_id):
    noticias = get_noticias(user_id)
    total_por_ticker = get_total_por_ticker(user_id)
    nome_usuario = nome_user(user_id)

    context = {
        'noticias': noticias,
        'total_por_ticker': total_por_ticker,
        'nome_usuario': nome_usuario
    }
    return render(request, 'index.html', context )

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        try:
            user_id = login_user(email, senha)
            if user_id:
                return redirect(reverse('index', kwargs={'user_id': user_id}))
        except:
            raise ValueError('Erro ao fazer o login')
    return render(request, 'login.html')

def chart_data(request):
    data = {
        'x': [1, 2, 3, 4, 5],
        'y': [random.randint(0, 100) for _ in range(5)]
    }
    return JsonResponse(data)

def index_view(request):
    return render(request, 'index.html')