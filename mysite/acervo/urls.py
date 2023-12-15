from django.urls import path
from . import views
from .views import LivroListView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'acervo'
urlpatterns = [
    path('', views.IndexView.as_view(), name = 'index'),
    path('livros/', views.LivroListView.as_view(), name='lista_livros'),
    path('livros/add/', views.NovoLivroView.as_view(), name='livro_add'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)