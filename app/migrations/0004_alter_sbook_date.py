# Generated by Django 4.1 on 2025-04-03 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_services_sbook_assign_sbook'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sbook',
            name='date',
            field=models.CharField(max_length=20),
        ),
    ]
