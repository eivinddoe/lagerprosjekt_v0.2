# Generated by Django 2.1.1 on 2018-09-12 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lager', '0005_auto_20180912_1112'),
    ]

    operations = [
        migrations.RenameField(
            model_name='artikkel',
            old_name='dtkost',
            new_name='vektet_risiko',
        ),
    ]
