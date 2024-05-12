# Generated by Django 4.2.9 on 2024-03-28 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_department_salary_after_deduction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='department',
            name='salary_after_deduction',
        ),
        migrations.AddField(
            model_name='employee',
            name='salary',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Salary',
        ),
    ]