from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('enquetes/<int:pergunta_id>/', views.detalhes, name='detalhes'),
    path('enquetes/<int:pergunta_id>/votacao/', views.votacao, name='votacao'),
    path('enquetes/<int:pergunta_id>/resultado/', views.resultado, name='resultado'),
    path('sobre/', views.sobre, name = 'sobre'),
]