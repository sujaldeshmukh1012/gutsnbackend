# Generated by Django 3.0.7 on 2021-05-27 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0019_auto_20210526_2256'),
    ]

    operations = [
        migrations.AddField(
            model_name='ipmodel',
            name='time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]