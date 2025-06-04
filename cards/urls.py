# cards/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('gastos/', views.lista_gastos, name='lista_gastos'),
    path('novo_gasto/', views.criar_gasto, name='novo_gasto'),
    path('novo_cartao/', views.criar_cartao, name='novo_cartao'),
    path('nova_pessoa/', views.cria_pessoa, name='nova_pessoa'),
    path('relatorio/', views.relatorio_por_mes_e_pessoa, name='relatorio_gastos'),
    path('editar/<int:gasto_id>/', views.editar_gasto, name='editar_gasto'),
    path('excluir/<int:gasto_id>/', views.excluir_gasto, name='excluir_gasto'),
    path('relatorio/pdf/', views.gerar_pdf_gastos, name='relatorio_pdf'),
]
