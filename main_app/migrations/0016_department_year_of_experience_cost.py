# Generated by Django 4.2.9 on 2024-03-30 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0015_rename_include_experience_and_overtime_department_add_experience_and_overtime'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='year_of_experience_cost',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
