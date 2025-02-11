# Generated by Django 5.0.7 on 2024-11-22 13:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CIGB', '0002_remove_envase_observaciones_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrdenFormulacion',
            fields=[
                ('id_orden_formulacion', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_producto', models.CharField(max_length=255)),
                ('concentracion', models.CharField(max_length=255)),
                ('actividad_biologica', models.CharField(max_length=255)),
                ('envase_primario', models.CharField(max_length=255)),
                ('volumen', models.CharField(max_length=255)),
                ('observaciones', models.CharField(max_length=255)),
                ('c_referencia', models.CharField(max_length=255)),
                ('reactivo', models.CharField(max_length=255)),
                ('cantidad', models.CharField(max_length=255)),
                ('id_IFA', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CIGB.ifa')),
                ('id_usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
