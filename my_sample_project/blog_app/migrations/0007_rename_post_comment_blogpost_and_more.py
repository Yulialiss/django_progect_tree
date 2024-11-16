# Generated by Django 5.1.3 on 2024-11-15 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0006_rename_blogpost_comment_post_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='post',
            new_name='blogpost',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='created_at',
            new_name='post_time',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='status',
        ),
        migrations.AddField(
            model_name='comment',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.CharField(max_length=200),
        ),
    ]
