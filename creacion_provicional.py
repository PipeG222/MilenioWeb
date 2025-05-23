#!/usr/bin/env python
"""
Script independiente para poblar TipoEmpresa, Zona y Área una única vez.
Ejecuta: python fill_locativos_once.py
"""
import os
import django


def main():
    # Ajusta al módulo de settings de tu proyecto
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'milenio.settings')
    django.setup()

    from ordenes.models import TipoEmpresa, Zona, Area

    # 1. Definir tipos de empresa
    tipos = [
        'Hospitales',
        'Planta de Sacrificio',
        'Empresa de granos',
        'Manufacturera',
        'Restaurante',
        'Casa',
    ]

    # 2. Definir zonas y su asignación a tipos de empresa
    zonas_data = {
        'Sala de espera': ['Hospitales', 'Restaurante', 'Casa', 'Empresa de granos', 'Manufacturera'],
        'Cocina': ['Hospitales', 'Restaurante', 'Casa'],
        'Oficina': tipos,
        'Almacén': ['Planta de Sacrificio', 'Empresa de granos', 'Manufacturera'],
        'Área de cirugía': ['Hospitales'],
        'Sala de cuidados intensivos': ['Hospitales'],
        'Sala de procesamiento': ['Planta de Sacrificio', 'Manufacturera'],
        'Laboratorio': ['Empresa de granos', 'Planta de Sacrificio'],
        'Baños': ['Hospitales', 'Restaurante', 'Casa', 'Empresa de granos', 'Manufacturera'],
        'Comedor': ['Hospitales', 'Empresa de granos', 'Manufacturera', 'Casa'],
    }

    # 3. Definir áreas por zona
    areas_data = {
        'Sala de espera': ['Asientos', 'Recepción', 'Mesas auxiliares'],
        'Cocina': ['Encimeras', 'Fregadero', 'Despensa'],
        'Oficina': ['Escritorio', 'Archivador', 'Sala de reuniones'],
        'Almacén': ['Estanterías', 'Pasillo 1', 'Zona de carga'],
        'Área de cirugía': ['Quirófano 1', 'Quirófano 2', 'Sala de esterilización'],
        'Sala de cuidados intensivos': ['Camas UCI', 'Monitores', 'Zona de enfermería'],
        'Sala de procesamiento': ['Líneas de producción', 'Zona de empaquetado'],
        'Laboratorio': ['Campana de extracción', 'Mesas de análisis', 'Almacenamiento de reactivos'],
        'Baños': ['Lavabos', 'Inodoros', 'Duchas'],
        'Comedor': ['Mesas de comedor', 'Área de autoservicio', 'Cocina satélite'],
    }

    # Ejecutar creación
    empresas = {}
    for nombre in tipos:
        obj, created = TipoEmpresa.objects.get_or_create(nombre=nombre)
        empresas[nombre] = obj
        print(f"TipoEmpresa '{nombre}' {'creado' if created else 'existía'}")

    for zona_nombre, tipos_lista in zonas_data.items():
        zona_obj, created = Zona.objects.get_or_create(nombre=zona_nombre)
        for tipo in tipos_lista:
            zona_obj.tipos_empresa.add(empresas[tipo])
        zona_obj.save()
        print(f"Zona '{zona_nombre}' asignada a {tipos_lista}")

        for area_nombre in areas_data.get(zona_nombre, []):
            area_obj, a_created = Area.objects.get_or_create(zona=zona_obj, nombre=area_nombre)
            print(f"  Área '{area_nombre}' {'creada' if a_created else 'existía'} en zona '{zona_nombre}'")

    print('Población inicial robusta completada.')


if __name__ == '__main__':
    main()
