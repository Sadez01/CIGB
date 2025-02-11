# Generated by Django 5.0.7 on 2024-11-22 16:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CIGB', '0003_ordenformulacion'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrdenEnvase',
            fields=[
                ('id_orden_envase', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_producto', models.CharField(max_length=255)),
                ('fecha_fabricacion', models.DateField(auto_now_add=True)),
                ('fecha_vence', models.DateField()),
                ('destino', models.CharField(max_length=255)),
                ('cantidad_envasar', models.CharField(max_length=255)),
                ('observaciones', models.CharField(max_length=255)),
                ('cliente', models.CharField(max_length=255)),
                ('material', models.CharField(max_length=255)),
                ('c_impresion', models.CharField(max_length=255)),
                ('c_referencia', models.CharField(max_length=255)),
                ('id_envase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CIGB.envase')),
                ('id_llenado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CIGB.llenado')),
                ('id_usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrdenLlenado',
            fields=[
                ('id_orden_llenado', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_producto', models.CharField(max_length=255)),
                ('concentracion', models.CharField(max_length=255)),
                ('actividad_biologica', models.CharField(max_length=255)),
                ('densidad', models.CharField(max_length=255)),
                ('envase_primario', models.CharField(max_length=255)),
                ('volumen_teorico', models.CharField(max_length=255)),
                ('volumen', models.CharField(max_length=255)),
                ('observaciones', models.CharField(max_length=255)),
                ('cliente', models.CharField(max_length=255)),
                ('material', models.CharField(max_length=255)),
                ('c_referencia', models.CharField(max_length=255)),
                ('id_IFA', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CIGB.ifa')),
                ('id_usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
