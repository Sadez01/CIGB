from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.utils.timezone import now
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Usuarios, Producto, Material, IFA, Formulacion, Llenado, Envase, Solicitud, Entrega
import json
from django.core.serializers.json import DjangoJSONEncoder
import os
import mimetypes
from django.db.models import Avg

class OrdenFormulacion(models.Model):
    id_orden_formulacion = models.AutoField(primary_key=True)
    id_IFA = models.ForeignKey(IFA, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.SET_NULL, null=True)
    tipo_producto = models.CharField(max_length=255)
    concentracion = models.CharField(max_length=255)
    actividad_biologica = models.CharField(max_length=255)
    envase_primario = models.CharField(max_length=255)
    volumen = models.CharField(max_length=255)
    observaciones = models.CharField(max_length=255)
    c_referencia = models.CharField(max_length=255)
    reactivo = models.CharField(max_length=255)
    cantidad = models.CharField(max_length=255)   


def add_orden_view(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')

    if request.method == 'POST':
        orden_type = {'formulacion':OrdenFormulacion()}
        orden = orden_type['formulacion']
        filtered_post = {k: v for k, v in request.POST.items() if k != 'nombre' and k != 'csrfmiddlewaretoken' and k != 'id_IFA' and k != 'id_usuario'}
        if 'formulacion' == 'formulacion':
            orden.id_IFA=IFA.objects.get(id_IFA = request.POST['id_IFA'])
            orden.id_usuario=Usuarios.objects.get(usuario=request.user.usuario)
        for k, v in filtered_post:
            setattr(orden, k, v)
        orden.save()
            
        try:
            return JsonResponse({'status': 'success', 'message': 'Formulación añadida.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Ocurrió un error: {str(e)}'})

def mod_ordenFormulacion_view(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')

    if request.method == 'POST':
        ordenFormulacion = Formulacion.objects.get(nombre=request.POST['nombre'])
        id_IFA = IFA.objects.get(id_IFA = request.POST['IFA'])
        vol_teorico = request.POST['vol_teorico']
        fecha_vence = request.POST['fecha_vence']
        consumo_IFA_UT = request.POST['consumo_IFA_UT']
        frascos_esperados = request.POST['frascos_esperados']

        try:
            ordenFormulacion.id_IFA = id_IFA
            ordenFormulacion.vol_teorico = vol_teorico
            ordenFormulacion.fecha_vence = fecha_vence
            ordenFormulacion.consumo_IFA_UT = consumo_IFA_UT
            ordenFormulacion.frascos_esperados =frascos_esperados
            ordenFormulacion.save()
            return JsonResponse({'status': 'success', 'message': 'Formulación modificada.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Ocurrió un error: {str(e)}'})

def ordenLlenado_view(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')
    ordenLlenado_data = Llenado.objects.all()
    ordenFormulacion_data = Formulacion.objects.all()
        
    return render(request, 'llenado.html', {'ordenLlenado_data':ordenLlenado_data, 'ordenFormulacion_data':ordenFormulacion_data})

def add_ordenLlenado_view(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')

    if request.method == 'POST':
        id_orden_formulacion = Formulacion.objects.get(id_orden_formulacion = request.POST['orden_formulacion'])
        fecha_llenado = request.POST['fecha_llenado']
        id_usuario = Usuarios.objects.get(usuario=request.user.usuario)
        cantidad_llenada = request.POST['cantidad_llenada']
        cantidad_revisada = request.POST['cantidad_revisada']
        existencias_llenada = request.POST['existencias_llenada']

        try:
            addon = Llenado(
                        id_orden_formulacion = id_orden_formulacion,
                        fecha_llenado = fecha_llenado,
                        id_usuario = id_usuario,
                        cantidad_llenada = cantidad_llenada,
                        cantidad_revisada = cantidad_revisada,
                        existencias_llenada = existencias_llenada,
                )
            addon.save()
            return JsonResponse({'status': 'success', 'message': 'Llenado añadido'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Ocurrió un error: {str(e)}'})

def mod_ordenLlenado_view(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')

    if request.method == 'POST':
        ordenLlenado = Llenado.objects.get(nombre=request.POST['target_orden'])
        id_orden_formulacion = Formulacion.objects.get(id_orden_formulacion = request.POST['orden_formulacion'])
        fecha_llenado = request.POST['fecha_llenado']
        cantidad_llenada = request.POST['cantidad_llenada']
        cantidad_revisada = request.POST['cantidad_revisada']
        existencias_llenada = request.POST['existencias_llenada']

        try:
            ordenLlenado.id_orden_formulacion = id_orden_formulacion
            ordenLlenado.fecha_llenado = fecha_llenado
            ordenLlenado.cantidad_llenada = cantidad_llenada
            ordenLlenado.cantidad_revisada = cantidad_revisada
            ordenLlenado.existencias_llenada = existencias_llenada
            ordenLlenado.save()
            return JsonResponse({'status': 'success', 'message': 'Llenado modificado.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Ocurrió un error: {str(e)}'})

def ordenEnvase_view(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')
    ordenEnvase_data = Envase.objects.all()
    ordenLlenado_data = Llenado.objects.all()
        
    return render(request, 'envase.html', {'ordenEnvase_data':ordenEnvase_data, 'ordenLlenado_data':ordenLlenado_data})

def add_ordenEnvase_view(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')

    if request.method == 'POST':
        id_orden_llenado = Llenado.objects.get(id_orden_llenado = request.POST['orden_llenado'])
        fecha_envase = request.POST['fecha_envase']
        id_usuario = Usuarios.objects.get(usuario=request.user.usuario)
        cantidad_envasar = request.POST['cantidad_envasar']
        destino = request.POST['destino']
        fecha_liberada = request.POST['fecha_liberada']
        cantidad_liberada = request.POST['cantidad_liberada']
        exist_liberada = request.POST['exist_liberada']

        try:
            addon = Envase(
                        id_orden_llenado = id_orden_llenado,
                        fecha_envase = fecha_envase,
                        id_usuario = id_usuario,
                        cantidad_envasar = cantidad_envasar,
                        destino = destino,
                        fecha_liberada = fecha_liberada,
                        cantidad_liberada = cantidad_liberada,
                        exist_liberada = exist_liberada,
                )
            addon.save()
            return JsonResponse({'status': 'success', 'message': 'Se ha creado el envase.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Ocurrió un error: {str(e)}'})

def mod_ordenEnvase_view(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')

    if request.method == 'POST':
        ordenEnvase = Envase.objects.get(nombre=request.POST['target_orden'])
        id_orden_llenado = Llenado.objects.get(id_orden_llenado = request.POST['orden_llenado'])
        fecha_envase = request.POST['fecha_envase']
        cantidad_envasar = request.POST['cantidad_envasar']
        destino = request.POST['destino']
        fecha_liberada = request.POST['fecha_liberada']
        cantidad_liberada = request.POST['cantidad_liberada']
        exist_liberada = request.POST['exist_liberada']

        try:
            ordenEnvase.id_orden_llenado = id_orden_llenado
            ordenEnvase.fecha_envase = fecha_envase
            ordenEnvase.cantidad_envasar = cantidad_envasar
            ordenEnvase.destino = destino
            ordenEnvase.fecha_liberada = fecha_liberada
            ordenEnvase.cantidad_liberada = cantidad_liberada
            ordenEnvase.exist_liberada = exist_liberada
            ordenEnvase.save()
            return JsonResponse({'status': 'success', 'message': 'Se ha modificado el envase.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Ocurrió un error: {str(e)}'})

