# Generated by Django 3.2.5 on 2021-07-12 18:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('livros', '0003_auto_20210712_1304'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoria',
            name='cor',
            field=models.CharField(default='#ffffff', max_length=7),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='livro',
            name='autor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='autor_livro', to='livros.autor'),
        ),
        migrations.AlterField(
            model_name='livro',
            name='ean',
            field=models.CharField(max_length=13, verbose_name='EAN'),
        ),
        migrations.AlterField(
            model_name='livro',
            name='edicao',
            field=models.PositiveSmallIntegerField(default=1, null=True, verbose_name='Edição'),
        ),
        migrations.AlterField(
            model_name='livro',
            name='isbn',
            field=models.CharField(max_length=13, verbose_name='ISBN'),
        ),
    ]
