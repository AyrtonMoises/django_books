# Generated by Django 3.2.5 on 2021-07-14 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('livros', '0008_promocoes_ativo'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Promocoes',
            new_name='Promocao',
        ),
    ]
