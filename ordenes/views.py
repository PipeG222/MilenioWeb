from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import AreaLocativa, EspecieUso, Higiene, HigieneUso, Material, OrdenLocativos, OrdenLocativoZona, OrdenLocativoArea, MaterialUso, OrdenServicio, Plaga, Producto ,TipoEmpresa , Zona ,Area
from .forms import OrdenLocativosForm, OrdenServicioForm
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

def ordenservicio_add(request):
    """
    Vista para crear una nueva OrdenServicio.
    Gestiona:
      - Formulario principal (OrdenServicioForm)
      - Productos → MaterialUso
      - Higiene → HigieneUso (sí/no)
      - Especies → EspecieUso (alto/medio/bajo)
      - Áreas locativas → M2M radio sí/no
    """
    if request.method == 'POST':
        form = OrdenServicioForm(request.POST, request.FILES)
        if form.is_valid():
            orden_servicio = form.save()

            # 1) Productos → MaterialUso
            MaterialUso.objects.filter(orden_servicio=orden_servicio).delete()
            for pid in request.POST.getlist('productos'):
                try:
                    prod = Producto.objects.get(pk=int(pid))
                except (ValueError, Producto.DoesNotExist):
                    continue
                qty = request.POST.get(f'cantidad_{pid}', '').strip()
                if not qty:
                    continue
                try:
                    cantidad = float(qty)
                except ValueError:
                    continue
                MaterialUso.objects.create(
                    orden_servicio=orden_servicio,
                    material=prod,
                    cantidad=cantidad
                )

            # 2) Higiene → HygieneUso (sí/no)
            # Borramos usos previos y creamos sólo los "sí"
            HigieneUso.objects.filter(orden_servicio=orden_servicio).delete()
            for h in Higiene.objects.all():
                val = request.POST.get(f'higiene_{h.id}')
                if val == 'si':
                    HigieneUso.objects.create(
                        orden_servicio=orden_servicio,
                        higiene=h
                    )

            # 3) Especies → EspecieUso (alto/medio/bajo)
            EspecieUso.objects.filter(orden_servicio=orden_servicio).delete()
            for p in Plaga.objects.filter(activa=True):
                if request.POST.get(f'especie_{p.id}_check'):
                    nivel = request.POST.get(f'especie_{p.id}_nivel')
                    if nivel in ('alto', 'medio', 'bajo'):
                        EspecieUso.objects.create(
                            orden_servicio=orden_servicio,
                            plaga=p,
                            nivel=nivel
                        )

            # 4) Áreas locativas → M2M radio sí/no
            seleccionadas = []
            for a in AreaLocativa.objects.all():
                if request.POST.get(f'area_{a.id}') == 'si':
                    seleccionadas.append(a.pk)
            orden_servicio.areaslocativas.set(seleccionadas)

            return redirect(reverse('ordenes:ordenservicio_change', args=[orden_servicio.pk]))
        # else: formulariode inválido; caerá al render de abajo mostrando errores

    else:
        form = OrdenServicioForm()

    # Preparamos datos para el template

    niveles = ['alto', 'medio', 'bajo']

    higiene_levels = []
    for h in Higiene.objects.all():
        higiene_levels.append({
            'obj': h,
            'sel': request.POST.get(f'higiene_{h.id}') if request.method == 'POST' else None
        })

    especies = []
    for p in Plaga.objects.filter(activa=True):
        especies.append({
            'obj':   p,
            'check': request.POST.get(f'especie_{p.id}_check') if request.method == 'POST' else None,
            'nivel': request.POST.get(f'especie_{p.id}_nivel') if request.method == 'POST' else None,
        })

    area_choices = []
    for a in AreaLocativa.objects.all():
        area_choices.append({
            'obj': a,
            'sel': request.POST.get(f'area_{a.id}') if request.method == 'POST' else None
        })

    return render(request, 'ordenes/ordenservicio_form.html', {
        'form':           form,
        'niveles':        niveles,
        'higiene_levels': higiene_levels,
        'especies':       especies,
        'area_choices':   area_choices,
        'title':          'Añadir Orden de Servicio',
    })
def ordenservicio_change(request, pk):
    obj = get_object_or_404(OrdenServicio, pk=pk)
    if request.method == 'POST':
        form = OrdenServicioForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            obj = form.save()
            # similar material usage processing
            MaterialUso.objects.filter(orden_servicio=obj).delete()
            for pid in request.POST.getlist('productos'):
                try:
                    mat = Material.objects.get(pk=int(pid))
                    qty = float(request.POST.get(f'cantidad_{pid}', 0))
                    MaterialUso.objects.create(orden_servicio=obj, material=mat, cantidad=qty)
                except Exception:
                    continue
            return redirect(reverse('ordenes:ordenservicio_change', args=[obj.pk]))
    else:
        form = OrdenServicioForm(instance=obj)
    usos = MaterialUso.objects.filter(orden_servicio=obj)
    return render(
        request,
        'ordenes/ordenservicio_form.html',
        {
            'form': form,
            'obj': obj,
            'usos': usos,
            'title': 'Editar Orden de Servicio'
        }
    )
