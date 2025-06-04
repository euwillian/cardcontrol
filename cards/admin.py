from django.contrib import admin
from cards.models import Pessoa, Cartao, Gasto

class CartaoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome', 'id')
    
class PessoaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome', 'id')

class GastosAdmin(admin.ModelAdmin):
    list_display = ('cartao', 'data_do_gasto', 'valor_total', 'qtd_parcelas', 'descricao', 'quem_gastou')
    search_fields = ('cartao__nome', 'data_do_gasto', 'quem_gastou__nome')


admin.site.register(Cartao, CartaoAdmin)
admin.site.register(Pessoa, PessoaAdmin)
admin.site.register(Gasto, GastosAdmin)
