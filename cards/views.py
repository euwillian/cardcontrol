from django.shortcuts import render, redirect, get_object_or_404
from .models import Gasto, Pessoa, Cartao
from .forms import GastoForm, PessoaForm, CartaoForm
from dateutil.relativedelta import relativedelta
from django.db.models import Sum
from django.utils import timezone

# para gerar pdf
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa



def lista_gastos(request):
    
    # Filtra só as pessoas do usuário logado
    pessoas = Pessoa.objects.filter(usuario=request.user)
    
    pessoa_id = request.GET.get('pessoa')  # Pega o ID da pessoa selecionada (se houver)

    # Busca gastos do usuário logado
    gastos = Gasto.objects.filter(usuario=request.user)

    # Se houver filtro por pessoa, aplica
    if pessoa_id:
        gastos = gastos.filter(quem_gastou_id=pessoa_id)

    gastos = gastos.order_by('-data_do_gasto')
    
    contexto = {
        'gastos': gastos,
        'pessoas': pessoas,
        'pessoa_id': pessoa_id,  # Envia a pessoa selecionada para o template
    }

    return render(request, 'cards/lista.html', contexto)
    
    
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Erro ao gerar PDF: %s' % pisa_status.err)
    return response


def gerar_pdf_gastos(request):
    pessoa_id = request.GET.get('pessoa')
    mes = request.GET.get('mes')  # também pegue o mês aqui

    gastos = Gasto.objects.filter(usuario=request.user)

    if pessoa_id:
        gastos = gastos.filter(quem_gastou_id=pessoa_id)

    if mes:
        try:
            ano, mes_num = map(int, mes.split('-'))
            gastos = gastos.filter(data_do_gasto__year=ano, data_do_gasto__month=mes_num)
        except:
            pass

    gastos = gastos.order_by('-data_do_gasto')

    total = gastos.aggregate(total=Sum('valor_total'))['total'] or 0  # calcula o total dos gastos

    pessoas = Pessoa.objects.filter(usuario=request.user)

    context = {
        'gastos': gastos,
        'pessoa_id': pessoa_id,
        'pessoas': pessoas,
        'usuario': request.user,
        'mes': mes,
        'total': total,
    }

    return render_to_pdf('cards/relatorio_pdf.html', context)



def criar_gasto(request):
    if request.method == 'POST':
        form = GastoForm(request.POST, usuario=request.user)
        if form.is_valid():
            gasto = form.save(commit=False)
            
            qtd_parcelas = gasto.qtd_parcelas
            valor_total = gasto.valor_total
            data_inicio = gasto.data_do_gasto

            valor_parcela = valor_total / qtd_parcelas

            for i in range(qtd_parcelas):
                data_parcela = data_inicio + relativedelta(months=i)
                descricao_parcela = f"{gasto.descricao} ({i+1}/{qtd_parcelas})"
                form.usuario = request.user
                novo_gasto = Gasto(
                    cartao=gasto.cartao,
                    data_do_gasto=data_parcela,
                    valor_total=valor_parcela,
                    qtd_parcelas=1,              # a parcela individual tem qtd_parcelas = 1
                    descricao=descricao_parcela,
                    quem_gastou=gasto.quem_gastou,
                    usuario = form.usuario       # usuário logado
                )
                
                novo_gasto.save()

            return redirect('lista_gastos')
    else:
        form = GastoForm(usuario=request.user) # usuário logado

    return render(request, 'cards/form.html', {'form': form})


def editar_gasto(request, gasto_id):
    gasto = get_object_or_404(Gasto, pk=gasto_id, usuario=request.user)
     # Busca o gasto pelo ID ou retorna 404, com base no usuario logado

    if request.method == 'POST':  # Se o formulário foi submetido
        form = GastoForm(request.POST, instance=gasto)  # Preenche o form com os dados enviados e o objeto existente
        if form.is_valid():
            form.save()  # Salva a atualização no banco
            return redirect('lista_gastos')  # Redireciona para a lista de gastos
    else:
        form = GastoForm(instance=gasto)  # Se for GET, exibe o form com os dados do gasto

    return render(request, 'cards/form.html', {'form': form})


def excluir_gasto(request, gasto_id):
    gasto = get_object_or_404(Gasto, pk=gasto_id, usuario=request.user)  # Busca o gasto com base no usuário logado
    if request.method == 'POST':
        gasto.delete()  # Exclui o registro
        return redirect('lista_gastos')
    return render(request, 'cards/confirmar_exclusao.html', {'gasto': gasto})  # Confirmação


def cria_pessoa(request):
    if request.method == 'POST':
        form = PessoaForm(request.POST, usuario=request.user)
        if form.is_valid():
            form = form.save(commit=False)  # ainda não salva no banco
            form.usuario = request.user     # associa ao usuário logado
            form.save()

            return redirect('lista_gastos')
    else:
        form = PessoaForm(usuario=request.user)

    return render(request, 'cards/nova_pessoa.html', {'form': form})


def criar_cartao(request):
    if request.method == 'POST':
        form = CartaoForm(request.POST, usuario=request.user)
        if form.is_valid():
            form = form.save(commit=False)
            form.usuario = request.user
            form.save()

            return redirect('lista_gastos')
    else:
        form = PessoaForm(usuario=request.user)

    return render(request, 'cards/novo_cartao.html', {'form': form})


def relatorio_por_mes_e_pessoa(request):
    # Faz o filtro do usuário logado no sistema
    gastos = Gasto.objects.filter(usuario=request.user)

    pessoa_id = request.GET.get('pessoa')   # vem do parâmetro na URL ?pessoa=1
    mes = request.GET.get('mes')            # vem do parâmetro ?mes=2025-05 (YYYY-MM)

    if pessoa_id:
        gastos = gastos.filter(quem_gastou_id=pessoa_id)

    if mes:
        # separar ano e mês
        try:
            ano, mes_num = map(int, mes.split('-'))
            gastos = gastos.filter(data_do_gasto__year=ano, data_do_gasto__month=mes_num)
        except:
            pass  # se tiver problema com a data, não filtra

    # somar o valor_total para mostrar quanto a pessoa deve no período
    total = gastos.aggregate(total=Sum('valor_total'))['total'] or 0

    pessoas = Pessoa.objects.filter(usuario=request.user)  # para popular o select de pessoas no filtro

    contexto = {
        'gastos': gastos,
        'total': total,
        'pessoas': pessoas,
        'pessoa_id': pessoa_id,
        'mes': mes,
    }

    return render(request, 'cards/relatorio.html', contexto)
