from django.db import models
from django.contrib.auth.models import User # Responsável por saber qual é o usuário logado

class Pessoa(models.Model):
    nome = models.CharField(max_length=15, blank=False, null=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=False) # Liga ao usuário logado (auth_user) do banco de dados
    criado_em = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return self.nome

class Cartao(models.Model):
    nome = models.CharField(max_length=15, blank=False, null=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    criado_em = models.DateTimeField(auto_now_add=True, null=False)
    
    def __str__(self):
        return self.nome
 
class Gasto(models.Model):
    cartao = models.ForeignKey(Cartao, on_delete=models.PROTECT, related_name='fk_nome_cartao')
    data_do_gasto = models.DateField(blank=False, null=False)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    qtd_parcelas = models.IntegerField(blank=False, null=False)
    descricao = models.CharField(max_length=30, blank=False, null=False)
    CATEGORIAS_CHOICES = [
        ('despesas_fixas', 'Despesas Fixas'),
        ('despesas_variaveis', 'Despesas Variáveis'),
        ('alimentacao', 'Alimentação'),
        ('educacao', 'Educação'),
        ('assinatura', 'Assinatura'),
        ('lazer', 'Lazer'),
        ('relacionamento', 'Relacionamento'),
        ('manutencao', 'Manutenção'),
        ('financeiro', 'Financeiro'),
    ]
    categoria = models.CharField(max_length=20, default='outros', choices=CATEGORIAS_CHOICES)
    quem_gastou = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='fk_nome_pessoa')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    criado_em = models.DateTimeField(auto_now_add=True, null=False)   # campo de controle de quando foi inserido o registro
    
    def __str__(self):
        return f'{self.data_do_gasto} - {self.quem_gastou} - {self.valor_total} - {self.descricao}'
