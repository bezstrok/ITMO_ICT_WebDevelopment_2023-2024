# Generated by Django 4.0.10 on 2024-02-04 07:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('manufacturer', '0003_remove_manufacturer_created_at_and_more'),
        ('product', '0001_initial'),
    ]
    
    operations = [
        migrations.AlterField(
            model_name='product',
            name='manufacturer',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name='products', to='manufacturer.manufacturer'
            ),
        ),
    ]