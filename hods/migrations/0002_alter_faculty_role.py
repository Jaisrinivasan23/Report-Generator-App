# Generated by Django 5.1.3 on 2024-11-16 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hods', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faculty',
            name='role',
            field=models.CharField(max_length=50),
        ),
    ]
