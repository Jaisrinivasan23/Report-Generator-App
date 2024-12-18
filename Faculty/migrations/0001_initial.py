# Generated by Django 5.1.3 on 2024-11-16 14:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hods', '0002_alter_faculty_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=255)),
                ('event_title', models.CharField(max_length=255)),
                ('objective', models.TextField()),
                ('event_date_time', models.DateTimeField()),
                ('venue', models.CharField(max_length=255)),
                ('gps_image', models.ImageField(blank=True, null=True, upload_to='gps_images/')),
                ('normal_image', models.ImageField(blank=True, null=True, upload_to='normal_images/')),
                ('department_name', models.CharField(max_length=255)),
                ('faculty_coordinator_name', models.CharField(max_length=255)),
                ('no_of_students_attended', models.IntegerField()),
                ('classes_attended', models.CharField(max_length=255)),
                ('approval_letter', models.FileField(upload_to='approval_letters/')),
                ('speaker_details', models.TextField()),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hods.faculty')),
            ],
        ),
    ]
