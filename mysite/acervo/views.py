from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from .models import Livro, Contato, Emprestimo, Item
from django.urls import reverse
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db import transaction


####INDEX

class IndexView(View):
   # template_name = 'acervo/index.html'
    def get (self, request, *args, **kwargs):
        return render(request, 'acervo/index.html')

#### LISTAGEM DE LIVROS CADASTRADOS

class LivroListView(View):

    def get (self, request, *args, **kwargs):
        acervo = Livro.objects.all()
        context = {'acervo': acervo}
        return render(request, 'acervo/lista_livros.html', context)

####CADASTRO DE LIVROS

#@method_decorator(login_required, name='dispatch')
class NovoLivroView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'acervo/novo_livro.html', {'user':request.user})

    def post(self, request, *args, **kwargs):
        titulo = request.POST['titulo']
        autor = request.POST['autor']
        ano = request.POST['ano']
        fotoCapa = request.FILES.get('fotoCapa')
        livro = Livro.objects.create(
            titulo = titulo,
            autor = autor,
            ano = ano,
            fotoCapa = fotoCapa,
            emprestado = False,
            user = request.user
        )
        livro.save()
        return redirect('acervo:home')

#####LOGIN E LOGOUT


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'acervo/login.html')

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('acervo:home')
        else:
            contexto = {'erro': 'Usuário ou senha inválidos!'}
            return render(request, 'acervo/login.html', contexto)

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('/')

###### CADASTRO USER

class CadastroView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'acervo/cadastro.html')

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['senha']
        first_name = request.POST['nome']
        email = request.POST['email']

        if User.objects.filter(username=username).exists():
            contexto = {'erro': 'Este username já existe!'}
            return render(request, 'acervo/cadastro.html', contexto)

        user = User.objects.create_user(username=username, password=password, first_name=first_name, email=email)
        user.save()
        return render(request, 'acervo/login.html')


#####HOME

@method_decorator(login_required, name='dispatch')
class HomeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        lista_itens = Item.objects.filter(user = user).order_by('nome')
        lista_livros = Livro.objects.filter(user = user).order_by('titulo')
        lista_contatos = Contato.objects.filter(user=user).order_by('nome_cont')
        lista_emp = Emprestimo.objects.filter(user=user, data_dev = None)
        emprestimos_cadastrados = lista_emp.count() > 0
        contexto = {
            'user': user,
            'lista_itens': lista_itens,
            'lista_livros': lista_livros,
            'lista_contatos': lista_contatos,
            'lista_emp': lista_emp,
            'emprestimos_cadastrados': emprestimos_cadastrados,
            }
        return render(request, 'acervo/home.html', contexto)

#####PESQUISAR

class PesquisarView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        pesquisa = request.GET.get('pesquisa')
        lista_itens = Item.objects.filter(nome__icontains = pesquisa, user = user)
        lista_livros = Livro.objects.filter(titulo__icontains = pesquisa, user = user)
        lista_contatos = Contato.objects.filter(nome_cont__icontains = pesquisa, user = user)
        contexto = {
            'lista_itens': lista_itens,
            'lista_livros': lista_livros,
            'lista_contatos': lista_contatos,
            'pesquisa':pesquisa
            }
        return render(request, 'acervo/pesquisa.html', contexto )


#####CADASTRO ITEM

class SaveItemView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'acervo/novo_item.html', {'user': request.user})

    def post(self, request, *args, **kwargs):
        nome = request.POST['nome']
        descricao = request.POST['descricao']
        item = Item.objects.create(
            nome = nome,
            descricao = descricao,
            emprestado = False,
            user = request.user
        )
        item.save()
        return redirect('acervo:home')

#####VIEW CADASTRO CONTATO

class SaveContatoView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'acervo/contato.html', {'user':request.user})

    def post(self, request, *args, **kwargs):
        nome_cont = request.POST['nome_cont']
        email = request.POST['email']
        telefone = request.POST['telefone']
        contato = Contato.objects.create(
            nome_cont = nome_cont,
            email = email,
            telefone = telefone,
            user = request.user
        )
        contato.save()
        return redirect('acervo:home')
        #continuar com base no que o professor fez ainda


####VIEWS PARA CRUD EMPRESTIMO
class EmprestimoView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        lista_itens = Item.objects.filter(user = user).order_by('nome')
        lista_livros = Livro.objects.filter(user = user).order_by('titulo')
        lista_contatos = Contato.objects.filter(user = user).order_by('nome_cont')

        contexto = {
            'lista_itens':lista_itens,
            'lista_livros':lista_livros,
            'lista_contatos':lista_contatos,
            'user':user,
        }
        return render(request, 'acervo/emprestimo.html', contexto)

    def post(self, request, *args, **kwargs):
        item_id = request.POST.get('item')
        livro_id = request.POST.get('livro')
        contato_id = request.POST.get('contato')

        if contato_id:
            contato = Contato.objects.get(id=contato_id)

        with transaction.atomic():
            if item_id == 'Selecionar item':
                item = None
            else:
                item = Item.objects.get(id = item_id)
                item.emprestado = True
                item.save()

            if livro_id == 'Selecionar livro':
                livro = None
            else:
                livro = Livro.objects.get(id = livro_id)
                livro.emprestado = True
                livro.save()

            emp = Emprestimo.objects.create(
                contato = contato,
                livro = livro,
                item = item,
                user = request.user
            )
            emp.save()

            if item:
                item.save()
            if livro:
                livro.save()

        return redirect('acervo:home')

class EmprestimoFinalizarView(View):
    def get(self, request, *args, **kwargs):
        emp = Emprestimo.objects.get(pk = kwargs['pk'])
        emp.data_dev = date.today()

        livro = emp.livro
        if livro:
            livro.emprestado = False
            livro.save()

        item = emp.item
        if item:
            item.emprestado = False
            item.save()

        emp.save()

        return redirect('acervo:home')

class RegistroEmprestimoView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        lista_emp = Emprestimo.objects.filter(user = user, data_dev__isnull = False)
        emprestimos_finalizados = lista_emp.exists()
        contexto = {'lista_emp': lista_emp, 'user': user, 'emprestimos_finalizados': emprestimos_finalizados}
        return render(request, 'acervo/registro_emprestimo.html', contexto)

# ####TESTE EMPRESTIMO VIEW COM LEO
# def registrar_emprestimo(request, livro_id):
#     livro = get_object_or_404(Livro, pk=livro_id)
#     contatos = Contato.objects.all()

#     if request.method == 'POST':
#         email = request.POST.get('email')
#         contato = request.POST.get('contato')
#         contato = Contato.objects.get(pk = contato)

#         # Salvando o empréstimo diretamente no banco de dados
#         emprestimo = Emprestimo.objects.create(livro=livro, contato=contato)

#         if emprestimo:
#             livro.livro_emprestado = True
#             livro.save()

#             messages.success(request, 'Empréstimo registrado com sucesso!')
#             return redirect('acervo_pessoal:lista_livros_emprestados')
#         else:
#             messages.error(request, 'Erro ao registrar empréstimo.')
#             return redirect('acervo:registrar_emprestimo.html')  # Substitua pelo nome correto da sua URL

#     return render(request, 'acervo/registrar_emprestimo.html', {'livro': livro,'contatos': contatos})


# def lista_livros_emprestados(request):
#     livros_emprestados = Livro.objects.filter(livro_emprestado=True)
#     total_livros_emprestados = livros_emprestados.count()

#     return render(request, 'acervo_pessoal/lista_livros_emprestados.html', {'livros_emprestados': livros_emprestados, 'total_livros_emprestados': total_livros_emprestados})


