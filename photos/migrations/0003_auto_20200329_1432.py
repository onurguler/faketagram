# Generated by Django 3.0.4 on 2020-03-29 14:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('photos', '0002_photo_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='image_filter',
            field=models.CharField(blank=True, choices=[('_1977', '1977'), ('aden', 'Aden'), ('brannan', 'Brannan'), ('brooklyn', 'Brooklyn'), ('clarendon', 'Clarendon'), ('earlybird', 'Earlybird'), ('gingham', 'Gingham'), ('hudson', 'Hudson'), ('inkwell', 'Inkwell'), ('kelvin', 'Kelvin'), ('lark', 'Lark'), ('lofi', 'Lo-Fi'), ('maven', 'Maven'), ('mayfair', 'Mayfair'), ('moon', 'Moon'), ('nashville', 'Nashville'), ('perpetua', 'Perpetua'), ('reyes', 'Reyes'), ('rise', 'Rise'), ('slumber', 'Slumber'), ('stinson', 'Stinson'), ('toaster', 'Toaster'), ('valencia', 'Valencia'), ('walden', 'Walden'), ('willow', 'Willow'), ('xpro2', 'X-pro II')], max_length=15),
        ),
        migrations.AlterField(
            model_name='photo',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to=settings.AUTH_USER_MODEL),
        ),
    ]
