#!/usr/bin/env python
"""
Script independiente para poblar Materiales una única vez.
Ejecuta: python mats.py
"""
import os
import django

def main():
    # 1. Configurar DJANGO_SETTINGS_MODULE antes de importar cualquier modelo
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'milenio.settings')
    django.setup()

    # 2. Importar el modelo correcto (Material) después de inicializar Django
    from ordenes.models import Material

    # 3. Lista de tuplas (nombre, unidad_medida) para crear varios materiales
    materiales = [
        ('Alambre', 'metros'),
        ('Clavo', 'kilogramos'),
        ('Tornillo', 'unidades'),
        ('Tuerca', 'unidades'),
        ('Cemento', 'sacos'),
        ('Ladrillo', 'unidades'),
        ('Madera', 'metros'),
        ('Pintura', 'litros'),
    ]

    for nombre, unidad in materiales:
        mat, creado = Material.objects.get_or_create(
            nombre=nombre,
            defaults={'unidad_medida': unidad}
        )
        if creado:
            print(f"Creado: {mat}")
        else:
            print(f"Ya existía: {mat}")

    print("Total de materiales en la BD:", Material.objects.count())


if __name__ == '__main__':
    main()
