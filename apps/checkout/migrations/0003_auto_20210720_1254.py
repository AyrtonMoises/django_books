# Generated by Django 3.2.5 on 2021-07-20 15:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0002_auto_20210719_1024'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pedido',
            options={'ordering': ['-id'], 'verbose_name': 'Pedido', 'verbose_name_plural': 'Pedidos'},
        ),
        migrations.AlterModelOptions(
            name='pedidoitem',
            options={'ordering': ['-id'], 'verbose_name': 'Item do pedido', 'verbose_name_plural': 'Itens do pedido'},
        ),
        migrations.AlterField(
            model_name='pedidoitem',
            name='pedido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pedido_itens', to='checkout.pedido', verbose_name='Pedido'),
        ),
    ]
