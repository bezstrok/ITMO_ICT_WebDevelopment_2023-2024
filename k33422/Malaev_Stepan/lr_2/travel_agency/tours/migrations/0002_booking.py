# Generated by Django 5.0 on 2023-12-25 00:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('tours', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    
    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(
                    choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')],
                    default='pending', max_length=10
                )),
                ('booking_date', models.DateTimeField(auto_now_add=True)),
                ('tour', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='tours.tour'
                )),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to=settings.AUTH_USER_MODEL
                )),
            ],
            options={
                'indexes': [models.Index(fields=['user', 'tour'], name='tours_booki_user_id_1a761b_idx')],
            },
        ),
    ]
