# Generated by Django 4.2.9 on 2024-03-22 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_alter_employee_birthdate_alter_employee_country_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vacation',
            name='approved',
        ),
        migrations.AddField(
            model_name='vacation',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default='Pending', max_length=15),
        ),
    ]
