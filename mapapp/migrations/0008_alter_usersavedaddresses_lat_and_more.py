# Generated by Django 4.1.1 on 2022-09-22 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mapapp", "0007_alter_usersavedaddresses_lat_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usersavedaddresses",
            name="lat",
            field=models.FloatField(default=None, verbose_name="Latitude"),
        ),
        migrations.AlterField(
            model_name="usersavedaddresses",
            name="lng",
            field=models.FloatField(default=None, verbose_name="Longitude"),
        ),
    ]