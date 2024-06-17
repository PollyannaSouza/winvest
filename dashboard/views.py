from django.shortcuts import render, redirect
from django.urls import reverse
from dashboard.src.login import login_user
from dashboard.src.user import todos_ativos

def index(request, user_id):
    params = todos_ativos(user_id)
    #todo chamar mais uma função, para pegar o nome do usuário e passar tambpem no params, existe uma muito parecida no arquivo de login

    print(params)
    return render(request, 'index.html', params) #todo pegar essas infos do parametros e colocar na tela com JINJA


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