# Generated by Django 5.0 on 2023-12-28 08:06

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('tours', '0003_tour_country'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    
    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('rating', models.IntegerField(
                    validators=[django.core.validators.MinValueValidator(1),
                                django.core.validators.MaxValueValidator(10)]
                )),
                ('comment_date', models.DateTimeField(auto_now_add=True)),
                ('tour', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='tours.tour'
                )),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL
                )),
            ],
            options={
                'indexes': [models.Index(fields=['user', 'tour'], name='tours_revie_user_id_eaf5eb_idx')],
            },
        ),
    ]
