# Generated by Django 4.0.6 on 2023-12-21 20:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acervo', '0003_rename_foto_capa_livro_fotodacapa'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='livro',
            name='user',
        ),
    ]
