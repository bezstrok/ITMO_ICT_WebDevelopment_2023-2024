# Generated by Django 5.0 on 2023-12-29 06:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('tours', '0004_review'),
    ]
    
    operations = [
        migrations.CreateModel(
            name='TourImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='tour_images/')),
                ('tour', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, related_name='images', to='tours.tour'
                )),
            ],
        ),
    ]
