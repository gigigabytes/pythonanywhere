from django.contrib import admin

from .models import Pergunta, Alternativa

admin.site.register(Pergunta)
admin.site.register(Alternativa)