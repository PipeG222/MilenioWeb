from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Material, OrdenLocativos, OrdenLocativoZona, OrdenLocativoArea, MaterialUso ,TipoEmpresa , Zona ,Area
from .forms import OrdenLocativosForm
from decimal import Decimal

def ordenlocativos_add(request):
    # (idéntica a la que ya tienes, sin tocar zonas/áreas en POST, solo materiales)
    if request.method == 'POST':
        print("=== POST recibido en ordenlocativos_add ===")
        print("request.POST:", dict(request.POST))
        form = OrdenLocativosForm(request.POST, request.FILES)
        print("Instanciado OrdenLocativosForm")
        if form.is_valid():
            print("form.is_valid() = True")
            obj = form.save()
            print(f"Objeto OrdenLocativos guardado con pk = {obj.pk}")

            # Borrar usos de materiales previos
            borrados = MaterialUso.objects.filter(orden_locativo=obj).delete()
            print("MaterialUso borrados previos:", borrados)

            # Procesar materiales del POST
            material_ids = request.POST.getlist('materiales')
            print("material_ids obtenidos de request.POST.getlist('materiales'):", material_ids)

            for mid in material_ids:
                try:
                    mid_int = int(mid)
                    mat = Material.objects.get(pk=mid_int)
                    print(f"Encontrado Material id={mid_int}: {mat}")
                except (ValueError, Material.DoesNotExist):
                    print(f"Material id inválido o no existe: {mid}")
                    continue

                qty_str = request.POST.get(f'cantidad_{mid}', '').strip()
                print(f"Cantidad para material {mid}: '{qty_str}'")
                if not qty_str:
                    print(f"  - No se proporcionó cantidad para material {mid}, se omite.")
                    continue

                try:
                    cantidad = float(qty_str)
                    print(f"  - Cantidad convertida a float: {cantidad}")
                except ValueError:
                    print(f"  - Valor de cantidad no numérico para material {mid}: '{qty_str}', se omite.")
                    continue

                uso = MaterialUso.objects.create(
                    orden_locativo=obj,
                    material=mat,
                    cantidad=cantidad
                )
                print(f"  - MaterialUso creado: id={uso.id}, material={mat.nombre}, cantidad={cantidad}")

            # Imprimir usos finales
            usos_finales = MaterialUso.objects.filter(orden_locativo=obj)
            print("MaterialUso finales en la BD para esta orden:")
            for uso in usos_finales:
                print(f"   • uso.id={uso.id}, material={uso.material.nombre} (id={uso.material.id}), cantidad={uso.cantidad}")

            return redirect(reverse('ordenes:ordenlocativos_change', args=[obj.pk]))
        else:
            print("form.is_valid() = False")
            print("Errores en OrdenLocativosForm:", form.errors)

    else:
        form = OrdenLocativosForm()
        print("GET en ordenlocativos_add, mostrando formulario vacío")

    return render(
        request,
        'ordenes/ordenlocativos_form.html',
        {
            'form': form,
            'title': 'Añadir Orden Locativos'
        }
    )
def ordenlocativos_change(request, pk):
    """
    Vista para editar una OrdenLocativos: 
    - Carga en uso_dict las cantidades guardadas de cada material.
    - Marca los checkboxes de materiales basándose en uso_dict.keys().
    - Al guardar, sobreescribe solo MaterialUso.
    """
    obj = get_object_or_404(OrdenLocativos, pk=pk)

    # Construyo uso_dict = { material_id: cantidad }
    usos = MaterialUso.objects.filter(orden_locativo=obj).select_related('material')
    uso_dict = {uso.material.id: uso.cantidad for uso in usos}

    if request.method == 'POST':
        print("=== POST recibido en ordenlocativos_change ===")
        print("request.POST completo:", dict(request.POST))

        form = OrdenLocativosForm(request.POST, request.FILES, instance=obj)
        print("Instanciado OrdenLocativosForm con data POST")

        if form.is_valid():
            print("form.is_valid() = True")
            obj = form.save()
            print(f"OrdenLocativos guardado (pk={obj.pk})")

            # Borro todos los registros previos de MaterialUso de esta orden
            borrados = MaterialUso.objects.filter(orden_locativo=obj).delete()
            print("MaterialUso borrados previos:", borrados)

            # Recorro los materiales marcados en el POST
            material_ids = request.POST.getlist('materiales')
            print("material_ids obtenidos de POST:", material_ids)

            for mid in material_ids:
                try:
                    mid_int = int(mid)
                    mat = Material.objects.get(pk=mid_int)
                    print(f"→ Encontrado Material id={mid_int}: {mat.nombre}")
                except (ValueError, Material.DoesNotExist):
                    print(f"→ Material id inválido o no existe: {mid}")
                    continue

                qty_str = request.POST.get(f'cantidad_{mid}', '').strip()
                print(f"Cantidad recibida para material {mid}: '{qty_str}'")
                if not qty_str:
                    print(f"  - No se proporcionó cantidad para material {mid}, se omite.")
                    continue

                try:
                    cantidad = float(qty_str)
                    print(f"  - Cantidad convertida a float: {cantidad}")
                except ValueError:
                    print(f"  - Valor de cantidad no numérico para material {mid}: '{qty_str}', se omite.")
                    continue

                uso_creado = MaterialUso.objects.create(
                    orden_locativo=obj,
                    material=mat,
                    cantidad=cantidad
                )
                print(f"  - MaterialUso creado: id={uso_creado.id}, cantidad={cantidad}")

            # Reconstruir uso_dict para recargar la página con datos actualizados
            usos = MaterialUso.objects.filter(orden_locativo=obj).select_related('material')
            uso_dict = {uso.material.id: uso.cantidad for uso in usos}
            print("Nuevo uso_dict tras guardar:", uso_dict)

            return redirect(reverse('ordenes:ordenlocativos_change', args=[obj.pk]))
        else:
            print("form.is_valid() = False")
            print("Errores en OrdenLocativosForm:", form.errors)

    else:
        # GET: instancio el formulario con los datos actuales e inicializo 'materiales'
        materiales_ids = list(usos.values_list('material__id', flat=True))
        form = OrdenLocativosForm(instance=obj, initial={'materiales': materiales_ids})
        print("=== GET en ordenlocativos_change ===")
        print("materiales_ids iniciales:", materiales_ids)
        print("uso_dict inicial:", uso_dict)

    # Antes de renderizar, imprimo para verificar qué se pasa al template
    print("=== DATOS para el template ===")
    print("form (fields iniciales):")
    for name, field in form.fields.items():
        initial = form.initial.get(name, None)
        print(f"  - {name}: initial = {initial}")
    print("uso_dict que se envía al template:", uso_dict)
    print("obj actual (OrdenLocativos):", obj)

    return render(request, 'ordenes/ordenlocativos_form.html', {
        'form': form,
        'title': f'Editar Orden Locativos #{obj.pk}',
        'uso_dict': uso_dict,
        'obj': obj,
    })

def api_zones_by_tipo(request, tipo_id):
    """
    Devuelve las zonas asociadas a un TipoEmpresa en JSON.
    """
    try:
        tipo = TipoEmpresa.objects.get(pk=tipo_id)
        zonas = list(Zona.objects.filter(tipos_empresa=tipo).values('id','nombre'))
    except TipoEmpresa.DoesNotExist:
        zonas = []
    return JsonResponse({'zonas': zonas})

def api_areas_by_zone(request, zone_id):
    """
    Devuelve las áreas asociadas a una Zona en JSON.
    """
    areas = list(Area.objects.filter(zona_id=zone_id).values('id','nombre'))
    return JsonResponse({'areas': areas})
