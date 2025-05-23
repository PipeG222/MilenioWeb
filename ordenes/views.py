from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import OrdenLocativos, OrdenLocativoZona, OrdenLocativoArea, MaterialUso ,TipoEmpresa , Zona ,Area
from .forms import OrdenLocativosForm


def ordenlocativos_add(request):
    if request.method == 'POST':
        form = OrdenLocativosForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            # Zonas y áreas asociadas
            obj.orden_zonas.all().delete()
            for zona in form.cleaned_data['zonas']:
                oz = OrdenLocativoZona.objects.create(orden_locativo=obj, zona=zona)
                # Agregar áreas marcadas
                for area in form.cleaned_data['areas']:
                    if area.zona == zona:
                        OrdenLocativoArea.objects.create(orden_zona=oz, area=area)
            # Materiales y cantidades
            MaterialUso.objects.filter(orden_locativo=obj).delete()
            for part in (form.cleaned_data.get('cantidad_material','') or '').split(','):
                if ':' in part:
                    mid, qty = part.split(':',1)
                    try:
                        MaterialUso.objects.create(
                            orden_locativo=obj,
                            material_id=int(mid),
                            cantidad=qty
                        )
                    except ValueError:
                        continue
            return redirect(reverse('admin:ordenes_ordenlocativos_change', args=[obj.pk]))
    else:
        form = OrdenLocativosForm()
    return render(request, 'ordenes/ordenlocativos_form.html', {'form': form, 'title': 'Añadir Orden Locativos'})


def ordenlocativos_change(request, pk):
    obj = get_object_or_404(OrdenLocativos, pk=pk)
    if request.method == 'POST':
        form = OrdenLocativosForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            obj = form.save()
            # Similar lógica de guardar zonas, áreas y materiales...
            return redirect(reverse('admin:ordenes_ordenlocativos_change', args=[obj.pk]))
    else:
        form = OrdenLocativosForm(instance=obj)
    return render(request, 'ordenes/ordenlocativos_form.html', {'form': form, 'title': f'Editar Orden Locativos #{pk}'})

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
