"""
URL configuration for CIGB project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import services_view, colection_view, main_view, about_view, contacts_view, login_view, autenticate_view, logout_view, CIGB_view, users_view, add_account_view, mod_user_view, products_view, add_product_view, mod_product_view, IFA_view, add_IFA_view, mod_IFA_view, delete_view, formulacion_view, add_formulacion_view, mod_formulacion_view, llenado_view, add_llenado_view, mod_llenado_view, envase_view, add_envase_view, mod_envase_view, request_view, add_request_view, mod_request_view, deliver_view, add_deliver_view, mod_deliver_view, ordenFormulacion_view, ordenLlenado_view, ordenEnvase_view, add_orden_view, mod_orden_view

urlpatterns = [
    path('servicios/', services_view),
    path('coleccion/', colection_view),
    path('', main_view),
    path('sobre_mi/', about_view),
    path('contactos/', contacts_view),
    path('login/', login_view),
    path('autenticar/', autenticate_view),
    path('cerrar_sesion/', logout_view),
    path('CIGB/', CIGB_view),
    path('usuarios/', users_view),
    path('add_account/', add_account_view),
    path('mod_user/', mod_user_view),
    path('productos/', products_view),
    path('add_product/', add_product_view),
    path('mod_product/', mod_product_view),
    path('IFA/', IFA_view),
    path('add_IFA/', add_IFA_view),
    path('mod_IFA/', mod_IFA_view),
    path('delete/', delete_view),
    path('formulacion/', formulacion_view),
    path('add_formulacion/', add_formulacion_view),
    path('mod_formulacion/', mod_formulacion_view),
    path('llenado/', llenado_view),
    path('add_llenado/', add_llenado_view),
    path('mod_llenado/', mod_llenado_view),
    path('envase/', envase_view),
    path('add_envase/', add_envase_view),
    path('mod_envase/', mod_envase_view),
    path('solicitudes/', request_view),
    path('add_request/', add_request_view),
    path('mod_request/', mod_request_view),
    path('entregas/', deliver_view),
    path('add_deliver/', add_deliver_view),
    path('mod_deliver/', mod_deliver_view),
    path('orden_formulacion/', ordenFormulacion_view),
    path('add_orden_formulacion/', lambda request: add_orden_view(request, tipo='formulacion')),
    path('mod_orden_formulacion/', lambda request: mod_orden_view(request, tipo='formulacion')),
    path('orden_llenado/', ordenLlenado_view),
    path('add_orden_llenado/', lambda request: add_orden_view(request, tipo='llenado')),
    path('mod_orden_llenado/', lambda request: mod_orden_view(request, tipo='llenado')),
    path('orden_envase/', ordenEnvase_view),
    path('add_orden_envase/', lambda request: add_orden_view(request, tipo='envase')),
    path('mod_orden_envase/', lambda request: mod_orden_view(request, tipo='envase')),
]

