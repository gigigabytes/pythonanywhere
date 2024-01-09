from django.db import models
from datetime import date
from django.utils import timezone
from django.contrib.auth.models import User

class Item(models.Model):
    nome = models.CharField(max_length = 50)
    descricao = models.CharField(max_length = 100, blank = True)
    emprestado = models.BooleanField()
    user = models.ForeignKey(User, on_delete = models.CASCADE, default = None)

    def __str__(self):
        return self.nome

class Livro(models.Model):
    titulo = models.CharField(max_length = 100)
    autor = models.CharField(max_length = 50)
    ano = models.IntegerField()
    emprestado = models.BooleanField()
    user = models.ForeignKey(User, on_delete = models.CASCADE, default = None)
    fotoCapa = models.ImageField(upload_to='livros_capas/', null = True, blank = True)

    def __str__(self):
       return self.titulo

class Contato(models.Model):
    nome_cont = models.CharField(max_length = 50, default = None)
    email = models.CharField(max_length = 50)
    telefone = models.CharField(max_length = 15, default = None)
    user = models.ForeignKey(User, on_delete = models.CASCADE, default = None)

    def __str__(self):
        return self.nome_cont

# class Emprestimo(models.Model):
#     data_emprestimo = models.DateField(auto_now_add=True)
#     item = models.ForeignKey(Item, on_delete = models.CASCADE, null = True, blank = True)
#     livro = models.ForeignKey(Livro, on_delete = models.CASCADE, null = True, blank = True)
#     contato = models.ForeignKey(Contato, on_delete = models.CASCADE)
#     user = models.ForeignKey(User, on_delete = models.CASCADE, default = None)

#     def __str__(self):
#         if self.item:
#             return f"{self.item.nome}"
#         else:
#             return f"{self.livro.titulo}"


class Emprestimo(models.Model):
    data_emp = models.DateField(default = date.today)
    data_dev = models.DateField(blank = True, null = True)
    item = models.ForeignKey(Item, on_delete = models.CASCADE, null = True, blank = True)
    livro = models.ForeignKey(Livro, on_delete = models.CASCADE, null = True, blank = True)
    contato = models.ForeignKey(Contato, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE, default = None)

    def __str__(self):
        if self.item:
            return f"{self.item.nome}"
        else:
            return f"{self.livro.titulo}"