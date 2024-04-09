# Generated by Django 4.0.10 on 2024-02-09 22:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('product', '0007_remove_productbatch_batch_number_and_more'),
        ('trade', '0001_initial'),
    ]
    
    operations = [
        migrations.AlterField(
            model_name='trade',
            name='product_batch',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name='trades', to='product.productbatch'
            ),
        ),
    ]
