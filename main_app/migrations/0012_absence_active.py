# Generated by Django 4.2.9 on 2024-03-28 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0011_remove_department_salary_after_deduction_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='absence',
            name='active',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]