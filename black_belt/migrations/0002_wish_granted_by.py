# Generated by Django 3.1.1 on 2020-09-18 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('black_belt', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wish',
            name='granted_by',
            field=models.ManyToManyField(related_name='granted_wishes', to='black_belt.User'),
        ),
    ]
