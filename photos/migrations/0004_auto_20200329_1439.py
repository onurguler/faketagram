# Generated by Django 3.0.4 on 2020-03-29 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0003_auto_20200329_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image_filter',
            field=models.CharField(blank=True, choices=[('normal', 'Normal'), ('_1977', '1977'), ('aden', 'Aden'), ('brannan', 'Brannan'), ('brooklyn', 'Brooklyn'), ('clarendon', 'Clarendon'), ('earlybird', 'Earlybird'), ('gingham', 'Gingham'), ('hudson', 'Hudson'), ('inkwell', 'Inkwell'), ('kelvin', 'Kelvin'), ('lark', 'Lark'), ('lofi', 'Lo-Fi'), ('maven', 'Maven'), ('mayfair', 'Mayfair'), ('moon', 'Moon'), ('nashville', 'Nashville'), ('perpetua', 'Perpetua'), ('reyes', 'Reyes'), ('rise', 'Rise'), ('slumber', 'Slumber'), ('stinson', 'Stinson'), ('toaster', 'Toaster'), ('valencia', 'Valencia'), ('walden', 'Walden'), ('willow', 'Willow'), ('xpro2', 'X-pro II')], max_length=15),
        ),
    ]