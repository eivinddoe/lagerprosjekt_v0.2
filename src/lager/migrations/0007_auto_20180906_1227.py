# Generated by Django 2.1.1 on 2018-09-06 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lager', '0006_auto_20180906_1220'),
    ]

    operations = [
        migrations.AddField(
            model_name='artikkel',
            name='planlagt_byttet',
            field=models.DateField(blank=True, null=True, verbose_name='Planlagt byttet'),
        ),
        migrations.AddField(
            model_name='artikkel',
            name='skal_byttes',
            field=models.CharField(blank=True, choices=[('Sikkert', 'Sikkert'), ('Usikkert', 'Usikkert')], max_length=10, null=True, verbose_name='Sikkert/usikkert bytte'),
        ),
    ]
