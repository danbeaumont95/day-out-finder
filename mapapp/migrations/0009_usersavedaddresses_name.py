# Generated by Django 4.1.1 on 2022-09-22 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mapapp", "0008_alter_usersavedaddresses_lat_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="usersavedaddresses",
            name="name",
            field=models.CharField(default="test", max_length=100, verbose_name="Name"),
            preserve_default=False,
        ),
    ]