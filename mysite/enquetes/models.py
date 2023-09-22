import datetime
from django.db import models
from django.utils import timezone

# Create your models here.

class Pergunta(models.Model): #definir classe e herança
    texto = models.CharField(max_length=150) #definir atributos
    data_pub = models.DateTimeField('Data de publicação')
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return '{} ({})'.format(self.texto, self.id)

    def was_published_recently(self):
        return self.data_pub >= timezone.now() - datetime.timedelta(days=1)


class Alternativa(models.Model):
    texto = models.CharField(max_length=80)
    quant_votos = models.IntegerField('Quantidade de votos', default=0)
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE) #em caso de remoção usar models.cascade
    ativo = models.BooleanField(default=True)
    def __str__(self):
        return '{} ({})'.format(self.texto, self.id)

