# Generated by Django 4.0.10 on 2024-02-03 09:06

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('manufacturer', '0002_initial'),
    ]
    
    operations = [
        migrations.RemoveField(
            model_name='manufacturer',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='manufacturer',
            name='updated_at',
        ),
    ]