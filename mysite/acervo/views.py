from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from .models import Livro, Contato, EmprestimoLivro, EmprestimoItem, Item
from django.urls import reverse
from django.contrib import messages
from django.views.generic.list import ListView

#from django.contrib.authdecorators import login_required
#from django.utils.decorators import method_decorator


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
        titulo_val = request.POST.get('titulo', None)
        autor_val = request.POST.get('autor', None)
        ano_val = request.POST.get('ano', None)
        fotodacapa_val = request.POST.get('fotodacapa', None)

        if titulo_val and autor_val and ano_val:
            Livro.objects.create(titulo = titulo_val, autor = autor_val, ano = ano_val, fotodacapa = fotodacapa_val)
            messages.success(request, 'Livro cadastrado com sucesso!')
            return HttpResponseRedirect(reverse('livros:livro-list'))

        else:
            messages.error(request, 'Necessário preencher todos os campos.')
            return render(request, 'acervo/novo_livro.html')


#continuar com base no que o professor fez ainda