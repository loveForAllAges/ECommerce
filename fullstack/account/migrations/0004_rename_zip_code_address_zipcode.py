# Generated by Django 4.2.5 on 2023-12-30 22:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_remove_user_wishlist_delete_wish'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='zip_code',
            new_name='zipcode',
        ),
    ]