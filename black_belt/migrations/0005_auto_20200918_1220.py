# Generated by Django 3.1.1 on 2020-09-18 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('black_belt', '0004_wish_granted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wish',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name=(2020, 9, 18, 12, 20, 41, 4, 262, 1)),
        ),
        migrations.AlterField(
            model_name='wish',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name=(2020, 9, 18, 12, 20, 41, 4, 262, 1)),
        ),
    ]
