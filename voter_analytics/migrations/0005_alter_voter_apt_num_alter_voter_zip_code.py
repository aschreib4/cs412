# Generated by Django 5.1.5 on 2025-04-04 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voter_analytics', '0004_alter_voter_date_registration_alter_voter_dob'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voter',
            name='apt_num',
            field=models.TextField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='voter',
            name='zip_code',
            field=models.IntegerField(max_length=10),
        ),
    ]
