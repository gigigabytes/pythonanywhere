from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Pergunta, Alternativa
from django.urls import reverse


def index(request):
    lista_perguntas = Pergunta.objects.order_by('-data_pub')
    contexto = { 'lista_perguntas' : lista_perguntas}
    return render(request, 'enquetes/index.html', contexto)

def detalhes(request, pergunta_id):
    pergunta = get_object_or_404(Pergunta, pk = pergunta_id)
    return render(request, 'enquetes/detalhes.html', {'pergunta': pergunta})

def votacao(request, pergunta_id):
    pergunta = get_object_or_404(Pergunta, pk = pergunta_id)
    try:
        alt_id = request.POST['alt_id']
        alt_escolhida = pergunta.alternativa_set.get(pk=alt_id)
    except (KeyError, Alternativa.DoesNotExist):
        contexto = {
            'pergunta': pergunta, 'error': 'Você precisa selecionar uma alternativa válida!'
        }
        return render(request, 'enquetes/detalhes.html', contexto)
    else:
        alt_escolhida.quant_votos += 1
        alt_escolhida.save()
        return HttpResponseRedirect(
            reverse('enquetes:resultado', args=(pergunta.id,))
        )

    #resposta = '<h1>Votação da enquete %s<h1>' % pergunta_id
    #return HttpResponse(resposta)


def resultado(request, pergunta_id):
    resposta = '<h1>Resultado da enquete %s<h1>' % pergunta_id
    return HttpResponse(resposta)


def sobre(request):
    return HttpResponse('&copy; DSWeb/TADS/CNAT/IFRN, 2023.')

"""
1ª versão da visão de index
def index(request):
    lista_perguntas = Pergunta.objects.order_by('-data_pub')
    resposta = '<br/>'.join([p.texto for p in lista_perguntas])
    return HttpResponse('<h1>%s</h1>'%resposta)

2ª versão da visão de index

from django.template import loader

def index(request):
    lista_perguntas = Pergunta.objects.order_by('-data_pub')
    template = loader.get_template('enquetes/index.html') #2 estágios onde carregar objeto para a memória e renderizar
    contexto = { 'lista_perguntas' : lista_perguntas}
    return HttpResponse(template.render(contexto, request))

1ª versão detalhes

from django.http import HttpResponse, Http404

def detalhes(request, pergunta_id):
#pode gerar uma exceção#
    try:
        pergunta = Pergunta.objects.get(id=pergunta_id)
    except Pergunta.DoesNotExist:
        raise Http404('Nenhuma enquete satisfaz esse critério.')
    return render(request, 'enquetes/detalhes.html', {'pergunta': pergunta})

"""
