# Generated by Django 5.1.3 on 2024-11-07 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0002_blogpost_image_alter_blogpost_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='slug',
            field=models.SlugField(default='dummy-slug', unique_for_date=True),
            preserve_default=False,
        ),
    ]