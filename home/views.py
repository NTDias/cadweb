from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .forms import *



def index(request):
    return render(request,'index.html')

def categoria(request):
    contexto = {
        'lista': Categoria.objects.all().order_by('-id'),
    }
    return render(request, 'categoria/lista.html',contexto)

def form_categoria(request):
    if request.method == 'POST':
       form = CategoriaForm(request.POST)                        # instancia o modelo com os dados do form
       if form.is_valid():                                       # faz a validação do formulário
            form.save()                                          # salva a instancia do modelo no banco de dados
            return redirect('categoria')                         # redireciona para a listagem
    else:                                                        # método é get, novo registro
        form = CategoriaForm()


    contexto = {
        'form':form,
    }
    return render(request, 'categoria/formulario.html', contexto)    


def editar_categoria(request, id):
    categoria = Categoria.objects.get(pk=id)
    if request.method == 'POST':
        # combina os dados do formulário submetido com a instância do objeto existente, permitindo editar seus valores.
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            categoria = form.save() # save retorna o objeto salvo
            return redirect('categoria') # redireciona para a listagem
    else:
         form = CategoriaForm(instance=categoria)
    return render(request, 'categoria/formulario.html', {'form': form,})

def remover_categoria(request, id):
    try:
        categoria = Categoria.objects.get(pk=id)
        categoria.delete() #delete deleta o objeto selecionado
        messages.success(request, 'Removido com sucesso') #mensagem de confirmação da exclusão
    except Categoria.DoesNotExist:
        messages.error(request, 'Não encontrado') #mensagem de quando o sistema não encontra o registro
        
    return redirect('categoria')

def detalhes_categoria(request, id):
    try:
        categoria = Categoria.objects.get(pk=id)
        return render(request, 'categoria/detalhes.html', {'item': categoria})
    except Categoria.DoesNotExist:
        messages.error(request, 'Não encontrado')
        return redirect('categoria')


def cliente(request):
    contexto = {
        'lista': Cliente.objects.all().order_by('-id')
    }
    return render(request, 'cliente/lista.html', contexto)

def form_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Operação Concluída !')
            return redirect('cliente')
    else:
        form = ClienteForm()
    return render(request, 'cliente/formulario.html', {'form': form})

def editar_cliente(request, id):
    try:
        cliente = Cliente.objects.get(pk=id)
    except Cliente.DoesNotExist:
        messages.error(request, 'Não encontrado')
        return redirect('cliente')

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Operação Concluída!')
            return redirect('cliente')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'cliente/formulario.html', {'form': form})
def remover_cliente(request, id):
    try:
        cliente = Cliente.objects.get(pk=id)
        cliente.delete()
        messages.success(request, 'Excluído com sucesso')
    except Cliente.DoesNotExist:
        messages.error(request, 'Não encontrado')
    return redirect('cliente')

def detalhes_cliente(request, id):
    try:
        cliente = Cliente.objects.get(pk=id)
        return render(request, 'cliente/detalhes.html', {'item': cliente})
    except Cliente.DoesNotExist:
        messages.error(request, 'Registro não encontrado')
        return redirect('cliente')
