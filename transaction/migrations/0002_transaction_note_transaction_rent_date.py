# Generated by Django 5.1.4 on 2024-12-12 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='note',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='rent_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]