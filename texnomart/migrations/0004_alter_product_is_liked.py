# Generated by Django 5.1 on 2024-08-29 12:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('texnomart', '0003_remove_product_slug'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='is_liked',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
