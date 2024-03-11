# Generated by Django 4.0.10 on 2024-01-30 04:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    
    dependencies = [
        ('broker', '0001_initial'),
        ('product', '0001_initial'),
    ]
    
    operations = [
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('status', models.CharField(
                    choices=[('open', 'Open'), ('closed', 'Closed'), ('pending', 'Pending')], default='open',
                    max_length=15
                )),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('broker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='broker.broker')),
                ('product_batch',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.productbatch')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]