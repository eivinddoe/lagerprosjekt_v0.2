# Generated by Django 2.1.1 on 2018-09-12 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lager', '0007_artikkel_tid'),
    ]

    operations = [
        migrations.AddField(
            model_name='artikkel',
            name='vektet_lagerkost',
            field=models.TextField(blank=True, null=True),
        ),
    ]
