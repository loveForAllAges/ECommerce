# Generated by Django 4.2.5 on 2023-12-25 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_rename_request_searchhistory_content_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='searchhistory',
            name='customer',
        ),
    ]