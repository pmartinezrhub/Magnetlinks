# Generated by Django 3.2.19 on 2024-10-28 01:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('magnetlinks', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='magnetlink',
            old_name='image',
            new_name='imagelink',
        ),
    ]
