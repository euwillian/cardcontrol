from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from cards.views import lista_gastos

def criar_usuario(request):
    if request.method == "POST":
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect('login')
    else:
        user_form = UserCreationForm()
    return render(request, 'accounts/novo_usuario.html', {'user_form': user_form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # usa o login do Django, que você importou
            return redirect('lista_gastos')
        else:
            login_form = AuthenticationForm(request, data=request.POST)  # form com dados para mostrar erro
    else:
        login_form = AuthenticationForm()  # form vazio no GET

    return render(request, 'accounts/login.html', {'login_form': login_form})

def logout_view(request):
    logout(request)
    return redirect('login')
    