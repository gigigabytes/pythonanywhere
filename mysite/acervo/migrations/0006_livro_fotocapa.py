# Generated by Django 4.0.6 on 2024-01-08 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acervo', '0005_emprestimo_remove_emprestimolivro_contato_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='livro',
            name='fotoCapa',
            field=models.ImageField(blank=True, null=True, upload_to='livros_capas/'),
        ),
    ]
