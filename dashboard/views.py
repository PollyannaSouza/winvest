from django.shortcuts import render, redirect
from django.urls import reverse
from dashboard.src.login import login_user
from django.http import JsonResponse

import random

from dashboard.src.user import get_total_por_ticker,get_noticias, nome_user, get_dados_grafico, get_cotacoes

def index(request, user_id):
    noticias = get_noticias(user_id)
    total_por_ticker = get_total_por_ticker(user_id)
    nome_usuario = nome_user(user_id)
    #cotacoes = get_cotacoes(total_por_ticker.keys())
    context = {
        'noticias': noticias,
        'total_por_ticker': total_por_ticker,
        'nome_usuario': nome_usuario,
        'user_id': user_id,
        #'cotacoes': cotacoes
    }
    return render(request, 'index.html', context)

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

def chart_data(request, user_id):
    total_por_ticker = get_total_por_ticker(user_id)
    labels, values = get_dados_grafico(total_por_ticker)
    data = {
        'values': values,
        'labels': labels
    }
    return JsonResponse(data)

def index_view(request):
    return render(request, 'index.html')