# Generated by Django 4.1.5 on 2023-02-19 13:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_remove_user_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='YT_Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('title', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='videos',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.yt_video'),
        ),
    ]
