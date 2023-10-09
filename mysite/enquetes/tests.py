import datetime
from django.test import TestCase
from django.utils import timezone

from .models import Pergunta

class PerguntaModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        o metodo was_published_recently() deve retornar False para questoes
        com data de publicacao no futuro

        """
        time = timezone.now()  + datetime.timedelta(days=30)
        future_question = Pergunta(data_pub=time)
        self.assertIs(future_question.was_published_recently(), False)


