# Generated by Django 2.2.5 on 2020-03-23 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20200220_1253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Completed', 'Completed'), ('Pending', 'Pending'), ('Error', 'Error'), ('Ongoing', 'Ongoing')], default='Pending', max_length=20),
        ),
    ]
