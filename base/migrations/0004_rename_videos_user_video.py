# Generated by Django 4.1.5 on 2023-02-19 13:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_yt_video_user_videos'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='videos',
            new_name='video',
        ),
    ]
