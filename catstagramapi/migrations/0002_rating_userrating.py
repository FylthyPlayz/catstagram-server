# Generated by Django 4.0.3 on 2022-03-08 19:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catstagramapi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='UserRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catstagramapi.post')),
                ('rating', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catstagramapi.rating')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catstagramapi.catstagramer')),
            ],
        ),
    ]
