# Generated by Django 5.2 on 2025-05-10 05:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoEmpresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Orden',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('tipo', models.CharField(choices=[('INSPECCION', 'Inspección General'), ('BENEFICIO', 'Inspección Planta Beneficio')], max_length=50)),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('en_proceso', 'En proceso'), ('finalizada', 'Finalizada')], default='pendiente', max_length=20)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.cliente')),
                ('trabajadores', models.ManyToManyField(to='usuarios.empleado')),
            ],
        ),
        migrations.CreateModel(
            name='InspeccionGeneral',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('especie_encontrada', models.TextField()),
                ('evidencias', models.TextField()),
                ('hallazgos_planta', models.TextField()),
                ('uso_plaguicidas', models.TextField()),
                ('observaciones', models.TextField(blank=True)),
                ('firma_operario', models.ImageField(blank=True, null=True, upload_to='firmas/')),
                ('firma_acompanante', models.ImageField(blank=True, null=True, upload_to='firmas/')),
                ('certificado', models.FileField(blank=True, null=True, upload_to='certificados/')),
                ('orden', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ordenes.orden')),
            ],
        ),
        migrations.CreateModel(
            name='DesinfeccionAmbientes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hallazgos', models.TextField()),
                ('zonas_servicio', models.TextField()),
                ('ingredientes', models.TextField()),
                ('observaciones', models.TextField(blank=True)),
                ('recomendaciones', models.TextField(blank=True)),
                ('firma_operario', models.ImageField(blank=True, null=True, upload_to='firmas/')),
                ('firma_acompanante', models.ImageField(blank=True, null=True, upload_to='firmas/')),
                ('certificado', models.FileField(blank=True, null=True, upload_to='certificados/')),
                ('orden', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ordenes.orden')),
            ],
        ),
        migrations.CreateModel(
            name='OrdenLocativos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_servicio', models.CharField(max_length=50)),
                ('lugares', models.TextField()),
                ('areas', models.TextField()),
                ('materiales', models.TextField()),
                ('observaciones', models.TextField(blank=True)),
                ('recomendaciones', models.TextField(blank=True)),
                ('firma_operario', models.ImageField(blank=True, null=True, upload_to='firmas/')),
                ('firma_acompanante', models.ImageField(blank=True, null=True, upload_to='firmas/')),
                ('certificado', models.FileField(blank=True, null=True, upload_to='certificados/')),
                ('orden', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ordenes.orden')),
            ],
        ),
    ]
