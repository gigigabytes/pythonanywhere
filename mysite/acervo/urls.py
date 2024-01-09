from django.urls import path
from . import views
from .views import LivroListView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


app_name = 'acervo'
urlpatterns = [
    path('', views.IndexView.as_view(), name = 'index'),

    #url que faz a listagem dos livros
    path('livros/', views.LivroListView.as_view(), name='lista_livros'),

    #url que realiza o cadastro dos livros
    path('livros/add/', views.NovoLivroView.as_view(), name='livro_add'),

    #url que realiza o cadastro dos usuarios
    path('cadastro/', views.CadastroView.as_view(), name='cadastro'),

    #url que realiza o login
    path('entrar/', views.LoginView.as_view(), name = 'login'),

    path('trocar_senha/', auth_views.PasswordChangeView.as_view(template_name='app/password_change.html'), name='password_change'),

    #url que leva pra home onde o usuário pode visualizar as informações
    path('home/', views.HomeView.as_view(), name = 'home'),

    #url para pesquisar
    path("home/pesquisar", views.PesquisarView.as_view(), name='pesquisa'),

    #url dos itens
    path('home/salvar/item', views.SaveItemView.as_view(), name='salva_item'),

    # urls dos contatos
    path('home/salvar/contato', views.SaveContatoView.as_view(), name='salva_contato'),

    # urls dos empréstimos

    path('home/salvar/emprestimo', views.EmprestimoView.as_view(), name='emprestimo'),
    path('<int:pk>/finalizar', views.EmprestimoFinalizarView.as_view(), name='finalizar'),
    path('home/registro', views.RegistroEmprestimoView.as_view(), name='registro_emprestimo'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)