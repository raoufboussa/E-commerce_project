# Generated by Django 2.2 on 2019-11-25 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20191124_2205'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='Item',
            new_name='item',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
