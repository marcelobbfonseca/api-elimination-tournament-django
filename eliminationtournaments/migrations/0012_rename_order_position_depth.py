# Generated by Django 4.2 on 2023-07-07 19:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eliminationtournaments', '0011_alter_position_right_position'),
    ]

    operations = [
        migrations.RenameField(
            model_name='position',
            old_name='order',
            new_name='depth',
        ),
    ]
