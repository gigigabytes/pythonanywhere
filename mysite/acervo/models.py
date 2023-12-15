from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

"""class Usuario(models.Model):
    nome = models.CharField(max_length=200)
    email = models.EmailField(max_length=250)
    senha = models.CharField(max_length=250)

    def __str__(self):
        return self.nome
"""

class Contato(models.Model):
    nome = models.CharField(max_length=200)
    email = models.EmailField(max_length=250)
    data_criacao = models.DateTimeField(auto_now=True)
    data_edicao = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.nome

class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    ano = models.CharField(max_length=10)
    emprestado = models.BooleanField(default=False)
    foto_capa = models.ImageField(upload_to='media/capas/', null = True, blank = True)
    data_criacao = models.DateTimeField(auto_now=True)
    data_edicao = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def get_id(self):
        return self.id

    def __str__(self):
        return self.titulo

class EmprestimoLivro(models.Model):
    data_inicio = models.DateTimeField(auto_now_add=True)
    devolucao = models.DateTimeField(auto_now=True)
    data_edicao = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    contato = models.ForeignKey(Contato, on_delete=models.CASCADE, default=None)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, default=None)
    emprestimo = models.BooleanField(default=True)

    def get_livro_id(self):
        return self.livro.id


class Item(models.Model):
    nome= models.CharField(max_length=150)
    descricao = models.CharField(max_length=200)
    emprestado = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now=True)
    data_edicao = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def get_id(self):
        return self.id

    def __str__(self):
        return self.nome


class EmprestimoItem(models.Model):
    data_inicio = models.DateTimeField(auto_now_add=True)
    devolucao = models.DateTimeField(auto_now=True)
    data_criacao = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    contato = models.ForeignKey(Contato, on_delete=models.CASCADE, default=None)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, default=None)
    emprestado = models.BooleanField(default=True)

    def get_item_id(self):
        return self.item.id
