from django.contrib import admin

from .models import Livro, Emprestimo, Contato, Item

admin.site.register(Item)
admin.site.register(Livro)
admin.site.register(Emprestimo)
admin.site.register(Contato)