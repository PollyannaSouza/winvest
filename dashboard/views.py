from django.shortcuts import render, redirect
from django.urls import reverse
from dashboard.src.login import login_user
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

import random

from dashboard.src.user import get_total_por_ticker,get_noticias, nome_user, get_dados_grafico, get_cotacoes, get_total_por_carteira

def index(request, user_id):
    noticias = get_noticias(user_id)
    total_por_ticker = get_total_por_ticker(user_id)
    total_por_carteira = get_total_por_carteira(user_id)
    nome_usuario = nome_user(user_id)
    cotacoes = get_cotacoes(total_por_ticker.keys())
    context = {
        'noticias': noticias,
        'total_por_ticker': total_por_ticker,
        'total_por_carteira': total_por_carteira,
        'nome_usuario': nome_usuario,
        'user_id': user_id,
        'cotacoes': cotacoes,
        'ativos': list(total_por_ticker.keys())
    }
    print(context['ativos'])
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


@csrf_exempt
def submit_form_compra(request):
    if request.method == 'POST':
        data = request.POST
        codigo_ativo = data.get('codigo_ativo')
        descricao_ativo = data.get('descricao_ativo')
        classe_risco = data.get('classe_risco')
        setor = data.get('setor')
        descricao_setor = data.get('descricao_setor')
        data_operacao = data.get('data_operacao')
        valor_unitario = data.get('valor_unitario')
        quantidade_total = data.get('quantidade_total')

        # Print data to console for debugging purposes
        print('Dados recebidos para compra:', {
            'codigo_ativo': codigo_ativo,
            'descricao_ativo': descricao_ativo,
            'classe_risco': classe_risco,
            'setor': setor,
            'descricao_setor': descricao_setor,
            'data_operacao': data_operacao,
            'valor_unitario': valor_unitario,
            'quantidade_total': quantidade_total,
        })

        response_data = {
            'message': 'Dados de compra recebidos com sucesso!',
            'dados': {
                'codigo_ativo': codigo_ativo,
                'descricao_ativo': descricao_ativo,
                'classe_risco': classe_risco,
                'setor': setor,
                'descricao_setor': descricao_setor,
                'data_operacao': data_operacao,
                'valor_unitario': valor_unitario,
                'quantidade_total': quantidade_total,
            }
        }
        return JsonResponse(response_data)
    return JsonResponse({'error': 'Método não permitido'}, status=405)

@csrf_exempt
def submit_form_venda(request):
    if request.method == 'POST':
        data = request.POST
        select_codigo = data.get('select_codigo')
        data_operacao = data.get('data_operacao')
        valor_unitario = data.get('valor_unitario')
        quantidade_total = data.get('quantidade_total')

        print('Dados recebidos para venda:', {
            'select_codigo': select_codigo,
            'data_operacao': data_operacao,
            'valor_unitario': valor_unitario,
            'quantidade_total': quantidade_total,
        })
        response_data = {
            'message': 'Dados de venda recebidos com sucesso!',
            'dados': {
                'select_codigo': select_codigo,
                'data_operacao': data_operacao,
                'valor_unitario': valor_unitario,
                'quantidade_total': quantidade_total,
            }
        }
        return JsonResponse(response_data)
    return JsonResponse({'error': 'Método não permitido'}, status=405)