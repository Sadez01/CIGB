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
from .models import Usuarios, Producto, Material, IFA, Formulacion, Llenado, Envase, Solicitud, Entrega, OrdenFormulacion, OrdenLlenado, OrdenEnvase
import json
from django.core.serializers.json import DjangoJSONEncoder
import os
import mimetypes
from django.db.models import Avg


def authenticate(request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(usuario=username)
        except UserModel.DoesNotExist:
            return None

        if user.check_password(password):
            return user

def services_view(request):
    return render(request, 'services.html')

def colection_view(request):
    return render(request, 'colection.html')

def main_view(request):
    return render(request, 'principal.html')

def about_view(request):
    return render(request, 'about.html')

def contacts_view(request):
    return render(request, 'contacts.html')

def login_view(request):
    users = Usuarios.objects.all()
    if not users:
        admin=Usuarios(nombre='Admin', apellidos='Admin Admin', email='admin@gmail.com', cargo='admin', tipo='admin', usuario = 'admin')
        admin.set_password('admin')
        admin.save()
    return render(request, 'login.html')

def CIGB_view(request):
    if not request.user.is_authenticated:
        users = Usuarios.objects.all()
        if not users:
            admin=Usuarios(nombre='Admin', apellidos='Admin Admin', email='admin@gmail.com', cargo='admin', tipo='admin', usuario = 'admin')
            admin.set_password('admin')
            admin.save()
        return render(request, 'login.html')
    return render(request, 'CIGB.html')

def autenticate_view(request):
    username = request.POST['user']
    password = request.POST['password']
    remember_me = request.POST.get('remember', False)  # Obtener el valor de "Remember Me"
      
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        response_data = {
            'status': 'success',
            'message': 'Inicio de sesión exitoso.'
        }
        return JsonResponse(response_data)
    else:
        response_data = {
            'status': 'error',
            'message': 'Nombre de usuario o contraseña incorrectos.'
        }
        return JsonResponse(response_data)
    
def logout_view(request):
    logout(request)
    return render(request, 'principal.html')

def users_view(request):
    if not request.user.is_authenticated:
        users = Usuarios.objects.all()
        if not users:
            admin=Usuarios(nombre='Admin', apellidos='Admin Admin', email='admin@gmail.com', cargo='admin', tipo='admin', usuario = 'admin')
            admin.set_password('admin')
            admin.save()
        return render(request, 'login.html')
    User = get_user_model()
    users = User.objects.all()
    user_data = []
    
    for user in users:
        user_dict = {
            'id': user.id_usuario,
            'nombre': user.nombre,
            'apellidos': user.apellidos,
            'email': user.email,
            'cargo': user.cargo,
            'tipo': user.tipo,
            'usuario': user.usuario,
        }
        
        user_dict['producto'] = user.producto.nombre if user.producto else 'todos'
        user_dict['id_producto'] = user.producto.id_producto if user.producto else 'todos'
        
        user_data.append(user_dict)
        
    products = Producto.objects.all()
    product_data = []
    for product in products:
        product_dict = {
            'id' : product.id_producto,
            'nombre': product.nombre,
        }
        product_data.append(product_dict)
        
    return render(request, 'users.html', {'product_data':product_data,'user_data':user_data})

def add_account_view(request):
    if not request.user.is_authenticated:
        users = Usuarios.objects.all()
        if not users:
            admin=Usuarios(nombre='Admin', apellidos='Admin Admin', email='admin@gmail.com', cargo='admin', tipo='admin', usuario = 'admin')
            admin.set_password('admin')
            admin.save()
        return render(request, 'login.html')
    if request.method == 'POST':
        nombre = request.POST['nombre']
        apellidos = request.POST['apellidos']
        email = request.POST['email']
        user_type = request.POST['user_type']
        cargo = request.POST['cargo']
        usuario = request.POST['usuario']
        password = request.POST['contraseña']

        username_exists = Usuarios.objects.filter(usuario=usuario).exists()
        email_exists = Usuarios.objects.filter(email=email).exists()

        
        if username_exists:
            return JsonResponse({'status': 'error', 'message': 'El usuario ya existe.'})
        elif email_exists:
            return JsonResponse({'status': 'error', 'message': 'El correo ya existe.'})
        else:
            try:
                registration = Usuarios(
                    nombre=nombre,
                    apellidos=apellidos,
                    email=email,
                    cargo=cargo,
                    tipo=user_type,
                    usuario=usuario,
                )
                
                if user_type != 'admin':
                    producto_id = request.POST['producto']
                    id_producto = Producto.objects.get(id_producto=producto_id)
                    registration.producto = id_producto
                
                registration.set_password(password)
                registration.save()
                return JsonResponse({'status': 'success', 'message': 'Se ha creado el usuario.'})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': f'Ocurrió un error: {str(e)}'})

    else:
        return render(request, 'users.html')

def mod_user_view(request):
    if not request.user.is_authenticated:
        users = Usuarios.objects.all()
        if not users:
            admin=Usuarios(nombre='Admin', apellidos='Admin Admin', email='admin@gmail.com', cargo='admin', tipo='admin', usuario = 'admin')
            admin.set_password('admin')
            admin.save()
        return render(request, 'login.html')
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Solo se permiten solicitudes POST'})

    try:
        nombre = request.POST['nombre']
        apellidos = request.POST['apellidos']
        email = request.POST['email']
        user_type = request.POST['user_type']
        cargo = request.POST['cargo']
        usuario = request.POST['usuario']
        password = request.POST.get('contraseña')  # Usa get() para manejar casos donde el campo pueda estar vacío
        target_user = request.POST['target_user']
        
        Users = get_user_model()
        user = Users.objects.get(usuario=target_user)
        
        # Actualiza los campos del usuario
        user.nombre = nombre
        user.apellidos = apellidos
        user.email = email
        user.cargo = cargo
        user.tipo = user_type
        user.usuario = usuario
        
        if password and password!='':
            user.set_password(password)
        
        if user_type != 'admin':
            producto_id = request.POST['producto']
            try:
                id_producto = Producto.objects.get(id_producto=producto_id)
                user.producto = id_producto
            except ObjectDoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'El producto seleccionado no existe'})
        
        user.save()
        
        return JsonResponse({'status': 'success', 'message': 'Se ha modificado el usuario.'})
    
    except ObjectDoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'El usuario objetivo no existe'})
    except KeyError as e:
        return JsonResponse({'status': 'error', 'message': f'Falta el parámetro {e} en la solicitud POST'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
    
def products_view(request):  
    if not request.user.is_authenticated:
        users = Usuarios.objects.all()
        if not users:
            admin=Usuarios(nombre='Admin', apellidos='Admin Admin', email='admin@gmail.com', cargo='admin', tipo='admin', usuario = 'admin')
            admin.set_password('admin')
            admin.save()
        return render(request, 'login.html')  
    products = Producto.objects.all()
    product_data = []
    for product in products:
        product_dict = {
            'id': product.id_producto,
            'nombre': product.nombre,
        }

        materials = Material.objects.filter(id_producto=product.id_producto)

        for material in materials:
            product_dict[material.tipo] = material.nombre

        product_data.append(product_dict)

    return render(request, 'products.html', {'data':product_data})

def add_product_view(request):
    if not request.user.is_authenticated:
        users = Usuarios.objects.all()
        if not users:
            admin=Usuarios(nombre='Admin', apellidos='Admin Admin', email='admin@gmail.com', cargo='admin', tipo='admin', usuario = 'admin')
            admin.set_password('admin')
            admin.save()
        return render(request, 'login.html')
    if request.method == 'POST':
        nombre = request.POST['nombre']
        
        filtered_post = {k: v for k, v in request.POST.items() if k != 'nombre' and k != 'csrfmiddlewaretoken'}
        
        producto = Producto(nombre=nombre)
        producto.save()
        
        id_producto = producto.id_producto
        
        if id_producto:
            for clave, valor in filtered_post.items():
                if valor!='':
                    material = Material(id_producto=producto, tipo=clave, nombre=valor)
                    material.save()
        return JsonResponse({'status': 'success', 'message': 'Se a añadido el producto.'})

    else:
        return render(request, 'products.html')
    
def mod_product_view(request):
    if not request.user.is_authenticated:
        users = Usuarios.objects.all()
        if not users:
            admin=Usuarios(nombre='Admin', apellidos='Admin Admin', email='admin@gmail.com', cargo='admin', tipo='admin', usuario = 'admin')
            admin.set_password('admin')
            admin.save()
        return render(request, 'login.html')
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Solo se permiten solicitudes POST'})

    try:
        nombre = request.POST['nombre']
        objetivo = request.POST['target_product']
        filtered_post = {k: v for k, v in request.POST.items() if k != 'nombre' and k != 'csrfmiddlewaretoken' and k != 'target_product'}
        
        producto = Producto.objects.get(nombre=objetivo)
        if nombre!=objetivo:
            producto.nombre=nombre
            producto.save()
        
        for clave, valor in filtered_post.items():
            try:
                material = Material.objects.get(id_producto=producto, tipo=clave)
            except:
                material = False           
            if material:
                if valor!='':
                    material.nombre=valor
                else:
                    material.delete()
            elif valor!='':
                material = Material(id_producto=producto, tipo=clave, nombre=valor)
                material.save()

        return JsonResponse({'status': 'success', 'message': 'Se ha modificado el producto.'})
    except ObjectDoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'El producto objetivo no existe'})
    except KeyError as e:
        return JsonResponse({'status': 'error', 'message': f'Falta el parámetro {e} en la solicitud POST'})
    except Exception as e:
         return JsonResponse({'status': 'error', 'message': str(e)})
    
def IFA_view(request):
    if not request.user.is_authenticated:
        users = Usuarios.objects.all()
        if not users:
            admin=Usuarios(nombre='Admin', apellidos='Admin Admin', email='admin@gmail.com', cargo='admin', tipo='admin', usuario = 'admin')
            admin.set_password('admin')
            admin.save()
        return render(request, 'login.html')
    if request.user.tipo=='user':
        IFA_data = IFA.objects.filter(id_usuario=Usuarios.objects.get(usuario=request.user.usuario))
        product_data = [request.user.producto]
    else:
        IFA_data = IFA.objects.all()
        product_data = Producto.objects.all()

        
    return render(request, 'IFA.html', {'product_data':product_data,'IFA_data':IFA_data})

def add_IFA_view(request):
    if not request.user.is_authenticated:
        users = Usuarios.objects.all()
        if not users:
            admin=Usuarios(nombre='Admin', apellidos='Admin Admin', email='admin@gmail.com', cargo='admin', tipo='admin', usuario = 'admin')
            admin.set_password('admin')
            admin.save()
        return render(request, 'login.html')
    if request.method == 'POST':
        lote = request.POST['lote']
        fecha_fabricacion = now().date()
        id_producto = Producto.objects.get(id_producto=request.POST['producto'])
        id_usuario = Usuarios.objects.get(usuario=request.user.usuario)
        volumen = request.POST['volumen']
        act_biologica = request.POST['act_biologica']
        act_espectral = request.POST['act_espectral']
        prot_total = request.POST['prot_total']
        act_total_UT = request.POST['act_total_UT']
        existencia_UT = request.POST['existencia_UT']
        existencia_vol_IFA = request.POST['existencia_vol_IFA']
        vol_form_liquido = request.POST['vol_form_liquido']
        dosis_esperadas = request.POST['dosis_esperadas']

        try:
            addon = IFA(
                lote = lote,
                fecha_fabricacion = fecha_fabricacion,
                id_producto = id_producto,
                id_usuario = id_usuario,
                volumen = volumen,
                act_biologica = act_biologica,
                act_espectral = act_espectral,
                prot_total = prot_total,
                act_total_UT = act_total_UT,
                existencia_UT = existencia_UT,
                existencia_vol_IFA = existencia_vol_IFA,
                vol_form_liquido = vol_form_liquido,
                dosis_esperadas = dosis_esperadas
            )
            addon.save()
            return JsonResponse({'status': 'success', 'message': 'Se ha creado el IFA.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Ocurrió un error: {str(e)}'})

def mod_IFA_view(request):
    if not request.user.is_authenticated:
        users = Usuarios.objects.all()
        if not users:
            admin=Usuarios(nombre='Admin', apellidos='Admin Admin', email='admin@gmail.com', cargo='admin', tipo='admin', usuario = 'admin')
            admin.set_password('admin')
            admin.save()
        return render(request, 'login.html')
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Solo se permiten solicitudes POST'})

    try:
        lote = request.POST['lote']
        volumen = request.POST['volumen']
        act_biologica = request.POST['act_biologica']
        act_espectral = request.POST['act_espectral']
        prot_total = request.POST['prot_total']
        act_total_UT = request.POST['act_total_UT']
        existencia_UT = request.POST['existencia_UT']
        existencia_vol_IFA = request.POST['existencia_vol_IFA']
        vol_form_liquido = request.POST['vol_form_liquido']
        dosis_esperadas = request.POST['dosis_esperadas']
        target_IFA = request.POST['target_IFA']
        
        ifa = IFA.objects.get(lote=target_IFA)
                 
        ifa.lote = lote
        ifa.volumen = volumen
        ifa.act_biologica = act_biologica
        ifa.act_espectral = act_espectral
        ifa.prot_total = prot_total
        ifa.act_total_UT = act_total_UT
        ifa.existencia_UT = existencia_UT
        ifa.existencia_vol_IFA = existencia_vol_IFA
        ifa.vol_form_liquido = vol_form_liquido
        ifa.dosis_esperadas = dosis_esperadas

        ifa.save()
        
        return JsonResponse({'status': 'success', 'message': 'Se ha modificado el IFA.'})
    
    except ObjectDoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'El IFA objetivo no existe'})
    except KeyError as e:
        return JsonResponse({'status': 'error', 'message': f'Falta el parámetro {e} en la solicitud POST'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@csrf_exempt
def delete_view(request):
    if not request.user.is_authenticated:
        users = Usuarios.objects.all()
        if not users:
            admin=Usuarios(nombre='Admin', apellidos='Admin Admin', email='admin@gmail.com', cargo='admin', tipo='admin', usuario = 'admin')
            admin.set_password('admin')
            admin.save()
        return render(request, 'login.html')
    if request.method == 'DELETE':
        data = json.loads(request.body)
        tabla=data.get('tabla')
        id=data.get('id')
        
        if tabla == 'Usuario':
            usuarios = get_user_model()
            user = usuarios.objects.get(id_usuario=id)
            user.delete()
            return JsonResponse({'status': 'success', 'message': 'Se a elimino el usuario.'})
        elif tabla == 'Producto':
            producto = Producto.objects.get(id_producto=id)
            producto.delete()
            return JsonResponse({'status': 'success', 'message': 'Se a elimino el producto.'})
        elif tabla == 'IFA':
            ifa = IFA.objects.get(id_IFA=id)
            ifa.delete()
            return JsonResponse({'status': 'success', 'message': 'Se a elimino correctamente.'})
        elif tabla == 'Formulacion':
            formulacion = Formulacion.objects.get(id_orden_formulacion=id)
            formulacion.delete()
            return JsonResponse({'status': 'success', 'message': 'Se a elimino correctamente.'})
        elif tabla == 'Llenado':
            llenado = Llenado.objects.get(id_orden_llenado=id)
            llenado.delete()
            return JsonResponse({'status': 'success', 'message': 'Se a elimino correctamente.'})
        elif tabla == 'Envase':
            envase = Envase.objects.get(id_orden_envase=id)
            envase.delete()
            return JsonResponse({'status': 'success', 'message': 'Se a elimino correctamente.'})
        elif tabla == 'Solicitud':
            solicitud = Solicitud.objects.get(id_solicitud=id)
            solicitud.delete()
            return JsonResponse({'status': 'success', 'message': 'Se a elimino correctamente.'})
        elif tabla == 'Entrega':
            entrega = Entrega.objects.get(id_entrega=id)
            entrega.delete()
            return JsonResponse({'status': 'success', 'message': 'Se a elimino correctamente.'}) 
        elif tabla == 'Orden_Formulacion':
            orden_formulacion = OrdenFormulacion.objects.get(id_orden_formulacion=id)
            orden_formulacion.delete()
            return JsonResponse({'status': 'success', 'message': 'Se a elimino correctamente.'}) 
        elif tabla == 'Orden_Llenado':
            orden_llenado = OrdenLlenado.objects.get(id_orden_llenado=id)
            orden_llenado.delete()
            return JsonResponse({'status': 'success', 'message': 'Se a elimino correctamente.'}) 
        elif tabla == 'Orden_Envase':
            orden_entrega = OrdenEnvase.objects.get(id_orden_envase=id)
            orden_entrega.delete()
            return JsonResponse({'status': 'success', 'message': 'Se a elimino correctamente.'}) 
    
def formulacion_view(request):
    if not request.user.is_authenticated:
        users = Usuarios.objects.all()
        if not users:
            admin=Usuarios(nombre='Admin', apellidos='Admin Admin', email='admin@gmail.com', cargo='admin', tipo='admin', usuario = 'admin')
            admin.set_password('admin')
            admin.save()
        return render(request, 'login.html')
    if request.user.tipo == 'user':
        ordenFormulacion_data = Formulacion.objects.filter(id_usuario=Usuarios.objects.get(usuario = request.user.usuario))
        IFA_data = IFA.objects.filter(id_usuario=Usuarios.objects.get(usuario = request.user.usuario))
    else:
        ordenFormulacion_data = Formulacion.objects.all()
        IFA_data = IFA.objects.all()
        
    return render(request, 'formulacion.html', {'ordenFormulacion_data':ordenFormulacion_data, 'IFA_data':IFA_data})

def add_formulacion_view(request):
    if not request.user.is_authenticated:
        users = Usuarios.objects.all()
        if not users:
            admin=Usuarios(nombre='Admin', apellidos='Admin Admin', email='admin@gmail.com', cargo='admin', tipo='admin', usuario = 'admin')
            admin.set_password('admin')
            admin.save()
        return render(request, 'login.html')

    if request.method == 'POST':
        id_IFA = IFA.objects.get(id_IFA = request.POST['IFA'])
        fecha_fab = now().date()
        id_usuario = Usuarios.objects.get(usuario=request.user.usuario)
        vol_teorico = request.POST['vol_teorico']
        fecha_vence = request.POST['fecha_vence']
        consumo_IFA_UT = request.POST['consumo_IFA_UT']
        frascos_esperados = request.POST['frascos_esperados']

        try:
            addon = Formulacion(
                        id_IFA = id_IFA,
                        fecha_fab = fecha_fab,
                        id_usuario = id_usuario,
                        vol_teorico = vol_teorico,
                        fecha_vence = fecha_vence,
                        consumo_IFA_UT = consumo_IFA_UT,
                        frascos_esperados = frascos_esperados
                )
            addon.save()
            return JsonResponse({'status': 'success', 'message': 'Formulación añadida.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Ocurrió un error: {str(e)}'})

def mod_formulacion_view(request):
    if not request.user.is_authenticated:
        users = Usuarios.objects.all()
        if not users:
            admin=Usuarios(nombre='Admin', apellidos='Admin Admin', email='admin@gmail.com', cargo='admin', tipo='admin', usuario = 'admin')
            admin.set_password('admin')
            admin.save()
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

def llenado_view(request):
    if not request.user.is_authenticated:
        users = Usuarios.objects.all()
        if not users:
            admin=Usuarios(nombre='Admin', apellidos='Admin Admin', email='admin@gmail.com', cargo='admin', tipo='admin', usuario = 'admin')
            admin.set_password('admin')
            admin.save()
        return render(request, 'login.html')
    if request.user.tipo=='user':
        ordenLlenado_data = Llenado.objects.filter(id_usuario=request.user)
        ordenFormulacion_data = Formulacion.objects.filter(id_usuario=request.user)
    else:
        ordenLlenado_data = Llenado.objects.all()
        ordenFormulacion_data = Formulacion.objects.all()
        
    return render(request, 'llenado.html', {'ordenLlenado_data':ordenLlenado_data, 'ordenFormulacion_data':ordenFormulacion_data})

def add_llenado_view(request):
    if not request.user.is_authenticated:
        users = Usuarios.objects.all()
        if not users:
            admin=Usuarios(nombre='Admin', apellidos='Admin Admin', email='admin@gmail.com', cargo='admin', tipo='admin', usuario = 'admin')
            admin.set_password('admin')
            admin.save()
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

def mod_llenado_view(request):
    if not request.user.is_authenticated:
        users = Usuarios.objects.all()
        if not users:
            admin=Usuarios(nombre='Admin', apellidos='Admin Admin', email='admin@gmail.com', cargo='admin', tipo='admin', usuario = 'admin')
            admin.set_password('admin')
            admin.save()
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

def envase_view(request):
    if not request.user.is_authenticated:
        users = Usuarios.objects.all()
        if not users:
            admin=Usuarios(nombre='Admin', apellidos='Admin Admin', email='admin@gmail.com', cargo='admin', tipo='admin', usuario = 'admin')
            admin.set_password('admin')
            admin.save()
        return render(request, 'login.html')
    if request.user.tipo=='user':
        ordenEnvase_data = Envase.objects.filter(id_usuario=request.user)
        ordenLlenado_data = Llenado.objects.filter(id_usuario=request.user)
    else:
        ordenEnvase_data = Envase.objects.all()
        ordenLlenado_data = Llenado.objects.all()
        
    return render(request, 'envase.html', {'ordenEnvase_data':ordenEnvase_data, 'ordenLlenado_data':ordenLlenado_data})

def add_envase_view(request):
    if not request.user.is_authenticated:
        users = Usuarios.objects.all()
        if not users:
            admin=Usuarios(nombre='Admin', apellidos='Admin Admin', email='admin@gmail.com', cargo='admin', tipo='admin', usuario = 'admin')
            admin.set_password('admin')
            admin.save()
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

def mod_envase_view(request):
    if not request.user.is_authenticated:
        users = Usuarios.objects.all()
        if not users:
            admin=Usuarios(nombre='Admin', apellidos='Admin Admin', email='admin@gmail.com', cargo='admin', tipo='admin', usuario = 'admin')
            admin.set_password('admin')
            admin.save()
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

def request_view(request):
    if not request.user.is_authenticated:
        users = Usuarios.objects.all()
        if not users:
            admin=Usuarios(nombre='Admin', apellidos='Admin Admin', email='admin@gmail.com', cargo='admin', tipo='admin', usuario = 'admin')
            admin.set_password('admin')
            admin.save()
        return render(request, 'login.html')
    if request.user.tipo=='user':
        request_data = Solicitud.objects.filter(id_usuario=request.user)
    else:
        request_data = Solicitud.objects.all()
    producto_data = Producto.objects.all()
    return render(request, 'solicitud.html', {'request_data':request_data, 'producto_data':producto_data})

def add_request_view(request):
    if not request.user.is_authenticated:
        users = Usuarios.objects.all()
        if not users:
            admin=Usuarios(nombre='Admin', apellidos='Admin Admin', email='admin@gmail.com', cargo='admin', tipo='admin', usuario = 'admin')
            admin.set_password('admin')
            admin.save()
        return render(request, 'login.html')

    if request.method == 'POST':
        producto = Producto.objects.get(id_producto = request.POST['producto'])
        presentacion = request.POST['presentacion']
        id_usuario = Usuarios.objects.get(usuario=request.user.usuario)
        destino = request.POST['destino']
        pais = request.POST['pais']
        firma = request.POST['firma']
        cantidad_solicitada = request.POST['cantidad_solicitada']
        observacion = request.POST['observacion']

        try:
            addon = Solicitud(
                        id_producto = producto,
                        presentacion = presentacion,
                        id_usuario = id_usuario,
                        pais = pais,
                        destino = destino,
                        firma = firma,
                        cantidad_solicitada = cantidad_solicitada,
                        observacion = observacion
                )
            addon.save()
            return JsonResponse({'status': 'success', 'message': 'Se ha creado la solicitud.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Ocurrió un error: {str(e)}'})

def mod_request_view(request):
    if not request.user.is_authenticated:
        users = Usuarios.objects.all()
        if not users:
            admin=Usuarios(nombre='Admin', apellidos='Admin Admin', email='admin@gmail.com', cargo='admin', tipo='admin', usuario = 'admin')
            admin.set_password('admin')
            admin.save()
        return render(request, 'login.html')

    if request.method == 'POST':
        solicitud = Solicitud.objects.get(id_solicitud=request.POST['target_request'])
        producto = Producto.objects.get(id_producto = request.POST['producto'])
        presentacion = request.POST['presentacion']
        destino = request.POST['destino']
        pais = request.POST['pais']
        firma = request.POST['firma']
        observacion = request.POST['observacion']
        try:
            solicitud.id_producto = producto
            solicitud.presentacion = presentacion
            solicitud.destino = destino
            solicitud.pais = pais
            solicitud.firma = firma
            solicitud.observacion = observacion
            solicitud.save()
            return JsonResponse({'status': 'success', 'message': 'Se ha modificado la solicitud.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Ocurrió un error: {str(e)}'})

def deliver_view(request):
    if not request.user.is_authenticated:
        users = Usuarios.objects.all()
        if not users:
            admin=Usuarios(nombre='Admin', apellidos='Admin Admin', email='admin@gmail.com', cargo='admin', tipo='admin', usuario = 'admin')
            admin.set_password('admin')
            admin.save()
        return render(request, 'login.html')
    if request.user.tipo == 'user':
        deliver_data = Entrega.objects.filter(id_usuario=request.user)
        request_data = Solicitud.objects.filter(id_usuario=request.user)
        envase_data = Envase.objects.filter(id_usuario=request.user)
    else:
        
        deliver_data = Entrega.objects.all()
        request_data = Solicitud.objects.all()
        envase_data = Envase.objects.all()
        
    return render(request, 'entrega.html', {'deliver_data':deliver_data, 'request_data':request_data, 'envase_data':envase_data})

def add_deliver_view(request):
    if not request.user.is_authenticated:
        users = Usuarios.objects.all()
        if not users:
            admin=Usuarios(nombre='Admin', apellidos='Admin Admin', email='admin@gmail.com', cargo='admin', tipo='admin', usuario = 'admin')
            admin.set_password('admin')
            admin.save()
        return render(request, 'login.html')

    if request.method == 'POST':
        solicitud = Solicitud.objects.get(id_solicitud = request.POST['solicitud'])
        envase = Envase.objects.get(id_orden_envase = request.POST['envase'])
        cantidad_entregada = request.POST['cantidad_entregada']
        id_usuario = Usuarios.objects.get(usuario=request.user.usuario)
        fecha_entrega = request.POST['fecha_entrega']
        
        try:
            addon = Entrega(
                        id_solicitud = solicitud,
                        id_orden_envase = envase,
                        id_usuario = id_usuario,
                        cantidad_entregada = cantidad_entregada,
                        fecha_entrega = fecha_entrega
                )
            addon.save()
            return JsonResponse({'status': 'success', 'message': 'Se ha creado la entrega.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Ocurrió un error: {str(e)}'})

def mod_deliver_view(request):
    if not request.user.is_authenticated:
        users = Usuarios.objects.all()
        if not users:
            admin=Usuarios(nombre='Admin', apellidos='Admin Admin', email='admin@gmail.com', cargo='admin', tipo='admin', usuario = 'admin')
            admin.set_password('admin')
            admin.save()
        return render(request, 'login.html')

    if request.method == 'POST':
        solicitud = Solicitud.objects.get(id_solicitud=request.POST['target_request'])
        producto = Producto.objects.get(id_producto = request.POST['producto'])
        presentacion = request.POST['presentacion']
        destino = request.POST['destino']
        pais = request.POST['pais']
        firma = request.POST['firma']
        observacion = request.POST['observacion']
        try:
            solicitud.id_producto = producto
            solicitud.presentacion = presentacion
            solicitud.destino = destino
            solicitud.pais = pais
            solicitud.firma = firma
            solicitud.observacion = observacion
            solicitud.save()
            return JsonResponse({'status': 'success', 'message': 'Se ha modificado la entrega.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': 'Ocurrió un error: {str(e)}'})

def ordenFormulacion_view(request):
    if not request.user.is_authenticated:
        users = Usuarios.objects.all()
        if not users:
            admin=Usuarios(nombre='Admin', apellidos='Admin Admin', email='admin@gmail.com', cargo='admin', tipo='admin', usuario = 'admin')
            admin.set_password('admin')
            admin.save()
        return render(request, 'login.html')
    if request.user.tipo == 'user':
        ordenFormulacion_data = OrdenFormulacion.objects.filter(id_usuario=request.user)
        IFA_data = IFA.objects.filter(id_usuario=request.user)
    else:
        ordenFormulacion_data = OrdenFormulacion.objects.all()
        IFA_data = IFA.objects.all()
        
    return render(request, 'ordenFormulacion.html', {'ordenFormulacion_data':ordenFormulacion_data, 'IFA_data':IFA_data})

def ordenLlenado_view(request):
    if not request.user.is_authenticated:
        users = Usuarios.objects.all()
        if not users:
            admin=Usuarios(nombre='Admin', apellidos='Admin Admin', email='admin@gmail.com', cargo='admin', tipo='admin', usuario = 'admin')
            admin.set_password('admin')
            admin.save()
        return render(request, 'login.html')
    if request.user.tipo == '':
        ordenLlenado_data = OrdenLlenado.objects.filter(id_usuario=request.user)
        IFA_data = IFA.objects.filter(id_usuario=request.user)
    else:
        ordenLlenado_data = OrdenLlenado.objects.all()
        IFA_data = IFA.objects.all()
        
    return render(request, 'ordenLlenado.html', {'ordenLlenado_data':ordenLlenado_data, 'IFA_data':IFA_data})


def ordenEnvase_view(request):
    if not request.user.is_authenticated:
        users = Usuarios.objects.all()
        if not users:
            admin=Usuarios(nombre='Admin', apellidos='Admin Admin', email='admin@gmail.com', cargo='admin', tipo='admin', usuario = 'admin')
            admin.set_password('admin')
            admin.save()
        return render(request, 'login.html')
    if request.user.tipo == 'user':
        ordenEnvase_data = OrdenEnvase.objects.filter(id_usuario=request.user)
        envase_data = Envase.objects.filter(id_usuario=request.user)
    else:
        ordenEnvase_data = OrdenEnvase.objects.all()
        envase_data = Envase.objects.all()
        
    return render(request, 'ordenEnvase.html', {'ordenEnvase_data':ordenEnvase_data, 'envase_data':envase_data})

def add_orden_view(request, tipo=None):
    if not request.user.is_authenticated:
        users = Usuarios.objects.all()
        if not users:
            admin=Usuarios(nombre='Admin', apellidos='Admin Admin', email='admin@gmail.com', cargo='admin', tipo='admin', usuario = 'admin')
            admin.set_password('admin')
            admin.save()
        return render(request, 'login.html')

    if request.method == 'POST':
        orden_type = {'formulacion':OrdenFormulacion(), 'llenado':OrdenLlenado(), 'envase':OrdenEnvase()}
        orden = orden_type[tipo]
        orden.id_usuario=Usuarios.objects.get(usuario=request.user.usuario)
        if tipo == 'formulacion' or tipo == 'llenado':
            orden.id_IFA=IFA.objects.get(id_IFA = request.POST['id_IFA'])
        elif tipo == 'envase':
            orden.id_envase=Envase.objects.get(id_orden_envase=request.POST['id_envase'])
        for k, v in request.POST.items():
            if k != 'nombre' and k != 'csrfmiddlewaretoken' and k != 'id_IFA' and k != 'id_usuario' and k != 'id_envase':
                setattr(orden, k, v)
        orden.save()
            
        try:
            return JsonResponse({'status': 'success', 'message': 'Orden añadida.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Ocurrió un error: {str(e)}'})

def mod_orden_view(request, tipo=None):
    if not request.user.is_authenticated:
        users = Usuarios.objects.all()
        if not users:
            admin=Usuarios(nombre='Admin', apellidos='Admin Admin', email='admin@gmail.com', cargo='admin', tipo='admin', usuario = 'admin')
            admin.set_password('admin')
            admin.save()
        return render(request, 'login.html')

    if request.method == 'POST':
        try:
            if tipo == 'formulacion':
                orden = OrdenFormulacion.objects.get(id_orden_formulacion=request.POST['target_orden'])
                orden.id_IFA=IFA.objects.get(id_IFA = request.POST['id_IFA'])
            elif tipo == 'llenado':
                orden = OrdenLlenado.objects.get(id_orden_llenado=request.POST['target_orden'])
                orden.id_IFA=IFA.objects.get(id_IFA = request.POST['id_IFA'])
            elif tipo == 'envase':
                orden = OrdenEnvase.objects.get(id_orden_envase=request.POST['target_orden'])
                orden.id_envase=Envase.objects.get(id_orden_envase = request.POST['id_envase'])
            for k, v in request.POST.items():
                if k != 'nombre' and k != 'csrfmiddlewaretoken' and k != 'id_IFA' and k != 'id_usuario' and k != 'target_orden' and k != 'id_envase':
                    setattr(orden, k, v)
            orden.save()
                
            return JsonResponse({'status': 'success', 'message': 'Orden modificada.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Ocurrió un error: {str(e)}'})