# Generated by Django 3.2.7 on 2021-09-20 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20210920_0818'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='category',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
