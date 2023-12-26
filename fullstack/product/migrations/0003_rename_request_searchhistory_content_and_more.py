# Generated by Django 4.2.5 on 2023-12-25 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_product_wish'),
    ]

    operations = [
        migrations.RenameField(
            model_name='searchhistory',
            old_name='request',
            new_name='content',
        ),
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.ManyToManyField(related_name='product_brands', to='product.brand'),
        ),
    ]