# Generated by Django 4.2.9 on 2024-03-30 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0016_department_year_of_experience_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='additional_hours',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='yearsOfExperienceCost',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
