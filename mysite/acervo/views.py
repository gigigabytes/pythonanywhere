from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from .models import Livro, Contato, EmprestimoLivro, EmprestimoItem, Item
from django.urls import reverse
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User


class IndexView(View):
   # template_name = 'acervo/index.html'
    def get (self, request, *args, **kwargs):
        return render(request, 'acervo/index.html')


class LivroListView(View):

    def get (self, request, *args, **kwargs):
        acervo = Livro.objects.all()
        context = {'acervo': acervo}
        return render(request, 'acervo/lista_livros.html', context)

#@method_decorator(login_required, name='dispatch')
class NovoLivroView(View):
    def get (self, request, *args, **kwargs):
        return render(request, 'acervo/novo_livro.html')

    def post (self, request, *args, **kwargs):
        titulo_val = request.POST.get('titulo')
        autor_val = request.POST.get('autor' )
        ano_val = request.POST.get('ano')
        fotodacapa_val = request.POST.get('fotodacapa')

        if titulo_val and autor_val and ano_val:
            Livro.objects.create(titulo = titulo_val, autor = autor_val, ano = ano_val, fotodacapa = fotodacapa_val)
            messages.success(request, 'Livro cadastrado com sucesso!')
            return HttpResponseRedirect(reverse('livros:lista_livros'))

        else:
            messages.error(request, 'Necessário preencher todos os campos.')
            return render(request, 'acervo/novo_livro.html')



class LoginView(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/acervo/dashboard')
        else:
            return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = self._authenticate_user(request, username, password)

        if user:
            login(request, user)
            return redirect('/acervo/dashboard')
        else:
            context = { 'error_message': 'Usuário ou senha incorretos!' }
            return render(request, self.template_name, context)

    def _authenticate_user(self, request, username, password):
        return authenticate(request, username=username, password=password)

class LogoutView(TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('/acervo')
'''

class RegisterView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/acervo/dashboard')
        else:
            return render(request, 'acervo/register.html')


     def post(self, request, *args, **kwargs):
        username = request.POST['user']
        email = request.POST['email']
        password = request.POST['password']

        if self._user_exists(email):
            context = {'error_message': 'Este usuário já existe.'}
        else:
            user = self._create_user(username, email, password)
            if user:
                return redirect('/acervo/entrar')

        return render(request, 'app/login.html', context)

    def _user_exists(self, email):
        return User.objects.filter(email=email).exists()

    def _create_user(self, username, email, password):
        try:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            return user
        except:
            return None
#continuar com base no que o professor fez ainda

'''