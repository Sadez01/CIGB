from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, unique=True)
class Material(models.Model):
    id_materiales = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255)
    
class CustomUserManager(BaseUserManager):
    def create_user(self, email, name=None, password=None, **extra_fields):
        if not email:
            raise ValueError(_('El correo electrónico es obligatorio'))
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, name, password, **extra_fields)

class Usuarios(AbstractBaseUser):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(_('nombre'), max_length=255)
    apellidos = models.CharField(_('apellidos'), max_length=255)
    email = models.EmailField(_('correo electrónico'), unique=True)
    cargo = models.CharField(_('cargo'), max_length=255)
    tipo = models.CharField(_('tipo'), max_length=255)
    usuario = models.CharField(_('usuario'), max_length=255, unique=True)
    contraseña = models.CharField(_('contraseña'), max_length=255)
    producto = models.ForeignKey('Producto', on_delete=models.SET_NULL, null=True, blank=True, related_name='usuarios')
    
    USERNAME_FIELD = 'usuario'
    REQUIRED_FIELDS = ['nombre', 'apellidos', 'cargo', 'tipo']

    class Meta:
        abstract = False
        verbose_name = _('usuario')
        verbose_name_plural = _('usuarios')

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        if self.tipo == 'admin':
            self.producto = None  # Para admins, establece el campo en None
        super().save(*args, **kwargs)

class IFA(models.Model):
    id_IFA = models.AutoField(primary_key=True)
    lote = models.CharField(max_length=255, unique=True)
    fecha_fabricacion = models.DateField()
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.SET_NULL, null=True)
    volumen = models.CharField(max_length=255)
    act_biologica = models.CharField(max_length=255)
    act_espectral = models.CharField(max_length=255)
    prot_total = models.CharField(max_length=255)
    act_total_UT = models.CharField(max_length=255)
    existencia_UT = models.CharField(max_length=255)
    existencia_vol_IFA = models.CharField(max_length=255)
    vol_form_liquido = models.CharField(max_length=255)
    dosis_esperadas = models.CharField(max_length=255)

class Formulacion(models.Model):
    id_orden_formulacion = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, unique=True)
    id_IFA = models.ForeignKey(IFA, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.SET_NULL, null=True)
    vol_teorico = models.CharField(max_length=255)
    fecha_fab = models.DateField()
    fecha_vence = models.DateField()
    consumo_IFA_UT = models.CharField(max_length=255)
    frascos_esperados = models.CharField(max_length=255)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.nombre=f'F_{self.id_IFA.lote}_{self.id_orden_formulacion}'
        super().save(*args, **kwargs)
class Llenado(models.Model):
    id_orden_llenado = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, unique=True)
    id_orden_formulacion = models.ForeignKey(Formulacion, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.SET_NULL, null=True)
    fecha_llenado = models.DateField()
    cantidad_llenada = models.CharField(max_length=255)
    cantidad_revisada = models.CharField(max_length=255)
    existencias_llenada = models.CharField(max_length=255)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.nombre=f'L_{self.id_orden_formulacion.nombre}_{self.id_orden_llenado}'
        super().save(*args, **kwargs)

class Envase(models.Model):
    id_orden_envase = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, unique=True)
    id_orden_llenado = models.ForeignKey(Llenado, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.SET_NULL, null=True)
    fecha_envase = models.DateField()
    cantidad_envasar = models.CharField(max_length=255)
    destino = models.CharField(max_length=255)
    fecha_liberada = models.DateField()
    cantidad_liberada = models.CharField(max_length=255)
    exist_liberada = models.CharField(max_length=255)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.nombre=f'E_{self.id_orden_llenado.nombre}_{self.id_orden_envase}'
        super().save(*args, **kwargs)

class Solicitud(models.Model):
    id_solicitud = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.SET_NULL, null=True)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    presentacion = models.CharField(max_length=255)
    destino = models.CharField(max_length=255)
    pais = models.CharField(max_length=255)
    firma = models.CharField(max_length=255)
    cantidad_solicitada = models.IntegerField()
    fecha_solicitud = models.DateField(auto_now_add=True)
    observacion = models.TextField()
    cantidad_pendiente = models.IntegerField(null=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.cantidad_pendiente:
            self.cantidad_pendiente=self.cantidad_solicitada
            super().save(*args, **kwargs)

class Entrega(models.Model):
    id_entrega = models.AutoField(primary_key=True)
    id_solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.SET_NULL, null=True)
    id_orden_envase = models.ForeignKey(Envase, on_delete=models.CASCADE)
    cantidad_entregada = models.IntegerField()
    fecha_entrega = models.DateField()
    
    def save(self, *args, **kwargs):
        if self.id_solicitud.cantidad_pendiente:
            self.id_solicitud.cantidad_pendiente-=int(self.cantidad_entregada)
            if self.id_solicitud.cantidad_pendiente<0:
                raise Exception('La cantidad de entrega exede la cantidad solicitada')
            self.id_solicitud.save()
            super().save(*args, **kwargs)
    
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

class OrdenLlenado(models.Model):
    id_orden_llenado = models.AutoField(primary_key=True)
    id_IFA = models.ForeignKey(IFA, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.SET_NULL, null=True)
    tipo_producto = models.CharField(max_length=255)
    concentracion = models.CharField(max_length=255)
    actividad_biologica = models.CharField(max_length=255)
    densidad = models.CharField(max_length=255)
    envase_primario = models.CharField(max_length=255)
    volumen_teorico = models.CharField(max_length=255)
    volumen = models.CharField(max_length=255)
    observaciones = models.CharField(max_length=255)
    cliente = models.CharField(max_length=255)
    material = models.CharField(max_length=255)
    c_referencia = models.CharField(max_length=255)
    
class OrdenEnvase(models.Model):
    id_orden_envase = models.AutoField(primary_key=True)
    id_envase = models.ForeignKey(Envase, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.SET_NULL, null=True)
    tipo_producto = models.CharField(max_length=255)
    fecha_fabricacion = models.DateField(auto_now_add=True)
    fecha_vence = models.DateField()
    destino = models.CharField(max_length=255)
    cantidad_envasar = models.CharField(max_length=255)
    observaciones = models.CharField(max_length=255)
    cliente = models.CharField(max_length=255)
    material = models.CharField(max_length=255)
    c_impresion = models.CharField(max_length=255)
    c_referencia = models.CharField(max_length=255)