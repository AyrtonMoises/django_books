# Generated by Django 3.2.5 on 2021-07-26 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livros', '0012_remove_livro_estoque'),
    ]

    operations = [
        migrations.AlterField(
            model_name='livro',
            name='ativo',
            field=models.BooleanField(default=True),
        ),
    ]
