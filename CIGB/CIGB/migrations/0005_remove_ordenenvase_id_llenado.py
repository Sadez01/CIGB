# Generated by Django 5.0.7 on 2024-11-23 00:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CIGB', '0004_ordenenvase_ordenllenado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordenenvase',
            name='id_llenado',
        ),
    ]
