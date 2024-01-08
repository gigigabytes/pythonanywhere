from django.urls import path
from . import views
from .views import LivroListView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


app_name = 'acervo'
urlpatterns = [
    path('', views.IndexView.as_view(), name = 'index'),
    path('livros/', views.LivroListView.as_view(), name='lista_livros'),
    path('livros/add/', views.NovoLivroView.as_view(), name='livro_add'),
    path('cadastro/', views.RegisterView.as_view(), name='register'),
    path('entrar/', views.LoginView.as_view(), name='login'),
    path('trocar_senha/', auth_views.PasswordChangeView.as_view(template_name='app/password_change.html'), name='password_change'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)