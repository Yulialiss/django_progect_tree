# Generated by Django 5.1.3 on 2024-11-19 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0002_post_remove_blogpost_slug'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Post',
        ),
        migrations.AddField(
            model_name='blogpost',
            name='status',
            field=models.CharField(choices=[('DR', 'Чернетка'), ('PB', 'Опубліковано')], default='DR', max_length=2),
        ),
    ]
