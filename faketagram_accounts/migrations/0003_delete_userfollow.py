# Generated by Django 3.0.4 on 2020-04-02 21:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('faketagram_accounts', '0002_delete_profile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserFollow',
        ),
    ]
