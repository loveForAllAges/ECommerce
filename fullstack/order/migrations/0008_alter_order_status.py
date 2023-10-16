# Generated by Django 4.2.5 on 2023-10-16 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(0, 'Создан'), (1, 'В обработке'), (2, 'Отправлен'), (3, 'Ожидает получения'), (4, 'Завершен'), (5, 'Отменен')], default=0),
        ),
    ]
