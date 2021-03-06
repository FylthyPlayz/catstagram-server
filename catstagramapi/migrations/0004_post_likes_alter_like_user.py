# Generated by Django 4.0.3 on 2022-03-22 15:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catstagramapi', '0003_alter_like_user_alter_rating_rating_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(related_name='likes', through='catstagramapi.Like', to='catstagramapi.catstagramer'),
        ),
        migrations.AlterField(
            model_name='like',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catstagramapi.catstagramer'),
        ),
    ]
