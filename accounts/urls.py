# accounts/urls.py
from django.urls import path
from . import views
# from accounts.views import criar_usuario
from django.shortcuts import redirect

# Função que redireciona para a página de login
def redirect_to_login(request):
    return redirect('login')

urlpatterns = [
    path('', redirect_to_login), # quando não tem nada na URL, vai para login
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.criar_usuario, name='register'),
]
