# Generated by Django 5.1.3 on 2024-11-19 07:44

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0004_post_remove_blogpost_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='status',
            field=models.CharField(choices=[('Draft', 'Чернетка'), ('Published', 'Опубліковано')], default='Draft', max_length=10),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='published_at',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
