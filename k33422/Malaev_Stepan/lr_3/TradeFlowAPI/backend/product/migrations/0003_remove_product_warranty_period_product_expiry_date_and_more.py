# Generated by Django 4.0.10 on 2024-02-06 12:16

import datetime

import django.db.models.deletion
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ('product', '0002_alter_product_manufacturer'),
    ]
    
    operations = [
        migrations.RemoveField(
            model_name='product',
            name='warranty_period',
        ),
        migrations.AddField(
            model_name='product',
            name='expiry_date',
            field=models.DateField(default=datetime.datetime(2024, 2, 6, 12, 16, 25, 354982, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='production_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='productbatch',
            name='product',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name='batches', to='product.product'
            ),
        ),
    ]
