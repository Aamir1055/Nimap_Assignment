# Generated by Django 4.2.15 on 2024-08-23 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0003_alter_project_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
