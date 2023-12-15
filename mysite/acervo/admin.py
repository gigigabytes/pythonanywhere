from django.contrib import admin

from .models import Contato, Livro, EmprestimoLivro, Item, EmprestimoItem

admin.site.register(Contato)
admin.site.register(Livro)
admin.site.register(EmprestimoLivro)
admin.site.register(Item)
admin.site.register(EmprestimoItem)