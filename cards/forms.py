from django import forms
from .models import Gasto, Pessoa, Cartao

class GastoForm(forms.ModelForm):
    class Meta:
    # nome do modelo no banco de dados
        model = Gasto
        fields = ['cartao', 'data_do_gasto', 'valor_total', 'qtd_parcelas', 'descricao', 'quem_gastou']
        
        widgets = {
            'cartao': forms.Select(attrs={'class': 'form-select'}),
            'data_do_gasto': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'valor_total': forms.NumberInput(attrs={'class': 'form-control'}),
            'qtd_parcelas': forms.NumberInput(attrs={'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'quem_gastou': forms.Select(attrs={'class': 'form-select'}),
        }
        
        
# Sobrescrevemos o método __init__ do formulário para personalizar os dados exibidos nos campos.
# O objetivo é filtrar os dados dos campos 'quem_gastou' e 'cartao' para que mostrem 
# apenas os registros relacionados ao usuário logado.
# Isso garante que um usuário só veja e selecione dados que pertencem a ele.

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)  # Remove o 'usuario' dos kwargs (se existir)
        super().__init__(*args, **kwargs)      # Inicializa o form padrão com os argumentos restantes

        if usuario:
            # Filtra os campos 'quem_gastou' e 'cartao' com base no usuário logado
            self.fields['quem_gastou'].queryset = Pessoa.objects.filter(usuario=usuario)
            self.fields['cartao'].queryset = Cartao.objects.filter(usuario=usuario)


class PessoaForm(forms.ModelForm):
    class Meta:
        model = Pessoa
        fields = ['nome']  # só o nome mesmo
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('usuario', None)  # pega o usuário que a view passar
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        pessoa = super().save(commit=False)
        if self.usuario:
            pessoa.usuario = self.usuario  # força o usuário logado
        if commit:
            pessoa.save()
        return pessoa


class CartaoForm(forms.ModelForm):
    class Meta:
    # nome do modelo no banco de dados
        model = Cartao
        fields = ['nome']
    
    widgets = {
        'nome': forms.TextInput(attrs={'class': 'form-control'})
    }
    
    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('usuario', None)  # pega o usuário que a view passar
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        cartao = super().save(commit=False)
        if self.usuario:
            cartao.usuario = self.usuario  # força o usuário logado
        if commit:
            cartao.save()
        return cartao