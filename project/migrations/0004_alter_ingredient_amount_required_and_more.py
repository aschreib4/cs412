# Generated by Django 5.1.5 on 2025-04-18 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_alter_ingredient_units'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='amount_required',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='owneditem',
            name='quantity',
            field=models.FloatField(),
        ),
    ]
