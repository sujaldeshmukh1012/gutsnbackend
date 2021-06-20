# Generated by Django 3.0.7 on 2021-05-26 12:09

import autoslug.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0013_auto_20210526_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='body',
            field=models.TextField(default=True, max_length=10000, verbose_name='Body'),
        ),
        migrations.AlterField(
            model_name='post',
            name='id',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from=models.TextField(max_length=500, null=True, verbose_name='Title'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.TextField(max_length=500, null=True, verbose_name='Title'),
        ),
    ]