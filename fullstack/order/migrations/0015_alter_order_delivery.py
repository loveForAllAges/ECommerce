# Generated by Django 4.2.5 on 2023-11-06 22:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0014_rename_delivery_type_order_delivery'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='order.delivery'),
        ),
    ]
