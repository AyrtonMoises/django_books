# Generated by Django 3.2.5 on 2021-07-16 14:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('livros', '0010_auto_20210716_1123'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrinho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carrinho_key', models.CharField(db_index=True, max_length=40, verbose_name='Chave do Carrinho')),
                ('quantidade', models.PositiveSmallIntegerField(default=1, verbose_name='Quantidade')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Valor')),
                ('livro', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='livros.livro', verbose_name='Livro')),
            ],
            options={
                'verbose_name': 'Item do carrinho',
                'verbose_name_plural': 'Itens dos carrinhos',
                'unique_together': {('carrinho_key', 'livro')},
            },
        ),
    ]
