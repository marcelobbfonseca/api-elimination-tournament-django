# Generated by Django 4.2 on 2023-06-23 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eliminationtournaments', '0004_alter_position_player'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='tournament_type',
            field=models.CharField(default='elimination', max_length=80),
        ),
    ]
