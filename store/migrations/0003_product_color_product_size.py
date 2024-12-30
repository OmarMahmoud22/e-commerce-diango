# Generated by Django 5.1.3 on 2024-12-20 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='color',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]