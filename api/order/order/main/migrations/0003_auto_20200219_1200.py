# Generated by Django 2.2.3 on 2020-02-19 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20200219_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='latitude',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='longitude',
            field=models.CharField(max_length=20),
        ),
    ]