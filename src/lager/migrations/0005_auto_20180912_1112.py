# Generated by Django 2.1.1 on 2018-09-12 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lager', '0004_auto_20180912_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artikkel',
            name='dtkost',
            field=models.TextField(blank=True, null=True),
        ),
    ]