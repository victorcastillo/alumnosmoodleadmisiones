from django.db import models
from django.contrib.auth.models import User


class Adicional( models.Model ):

  usuario           = models.OneToOneField( User )
  apellido_materno  = models.CharField( max_length = 50, blank=True )
  matricula         = models.CharField(max_length=250, unique=True)
  fecha_cambio_estado = models.DateTimeField(null=True, blank=True)
  # entidad_negocio_principal = models.ForeignKey('EntidadNegocio', null=True, blank=True)
  exportado = models.BooleanField(default=False, db_index=True)
  fecha_matriculacion = models.DateTimeField(null=True, blank=True)

  def __unicode__(self):
    return str(self.id) + ' | ' + self.usuario.email

  class Meta:
    managed = False
    db_table = 'registro_adicional'


class Cat_Estado(models.Model):
  ESTADOS_TRAMITE_SA = (78, 79, 80, 81, 82, 83, 84)
  ESTADO_TRAMITE_CREDENCIAL = (102, 103, 104, 105, 106, 107, 108, 109)
  BAJA_DEFINITIVA = 94
  PROSPECTO = 50

  estado = models.CharField(max_length=100)
  contexto = models.CharField(max_length=100)

  def __unicode__(self):
    return self.estado + ' | ' + self.contexto

  class Meta:
  	managed = False
  	db_table = 'registro_cat_estado'

class Ciclo(models.Model):
  fecha_inicio = models.DateField()
  fecha_fin = models.DateField()
  fecha_limite_decision = models.DateField(default=None, null=True)
  clave_ciclo = models.CharField(max_length=10)
  habilitado = models.BooleanField()
  modalidad = models.ForeignKey('Modalidad', null=True)
  etiqueta = models.CharField(max_length=256)
  anio_academico = models.CharField(max_length='12', null=True, blank=True)
  periodo_academico = models.CharField(max_length='10', null=True, blank=True)
  sesion_academico = models.CharField(max_length='10', null=True, blank=True)

  def __unicode__(self):
    return self.clave_ciclo

  class Meta:
    managed = False
    db_table = 'registro_ciclo'


class InscripcionCiclo(models.Model):
  INSCRIPCIONCICLO_CANCELADA = 57
  INSCRIPCIONCICLO_INACTIVA = 66
  PAGADO = 56
  PENDIENTE_PAGO = 55

  inscripcion = models.ForeignKey('Inscripcion')
  ciclo = models.ForeignKey('Ciclo')
  fecha_registro = models.DateTimeField(auto_now_add=True)
  cat_estado = models.ForeignKey('Cat_Estado')
  usuario = models.ForeignKey(User)


  class Meta:
    managed = False
    db_table = 'registro_inscripcionciclo'



class Modalidad(models.Model):
  MOD_LICENCIATURA = 1
  MOD_EC_DIPLOMADO = 2
  MOD_EC_CURSO = 3
  MOD_EC_CERTIFICACION = 4
  MOD_MAESTRIA = 5
  MOD_LICENCIATURA_EJECUTIVA = 6
  MOD_LICENCIATURA_MENTOREO = 7
  MOD_EC_INGLES = 8

  MOD_HE = (MOD_LICENCIATURA, MOD_MAESTRIA, MOD_LICENCIATURA_EJECUTIVA, MOD_LICENCIATURA_MENTOREO)
  MOD_STUDENT = (MOD_EC_DIPLOMADO, MOD_EC_CURSO, MOD_EC_CERTIFICACION)

  modalidad = models.CharField(max_length=100)
  # contrato = models.TextField()
  # matricula_requerida = models.BooleanField(default=True)
  # nomenclatura_periodo = models.CharField(max_length=256)
  # aplica_reinscripcion = models.BooleanField(default=False)
  # permite_autoinscripcion = models.BooleanField(default=False)
  # clave_power_campus = models.CharField(max_length=10, null=True, blank=True)
  # long_referencia = models.IntegerField()
  # permite_autoreinscripcion = models.BooleanField(default=False)
  # sites = models.ManyToManyField(Site, through='ModalidadSite')
  # metodos_pago = models.ManyToManyField('MetodoPago', through='ModalidadesMetodosPago')
  # hay_periodo_ingreso = models.BooleanField(default=False)
  # aplica_credencial = models.BooleanField(default=False)
  # objects = ModalidadManager()
  # 
  def __unicode__(self):
  	return self.modalidad
  
  class Meta:
  	managed = False
  	db_table = 'registro_modalidad'


class Inscripcion(models.Model):

  modalidad = models.ForeignKey('Modalidad', null=True)
  usuario = models.ForeignKey(User)
  # alta =  models.DateField(auto_now_add=True)
  # cat_estado = models.ForeignKey(Cat_Estado, verbose_name=_('Estado'))
  # ciclo = models.ForeignKey(Ciclo, null=True, blank=True)
  # licenciatura = models.ForeignKey(Licenciatura, null=True)
  cat_estado_usuario_inscripcion = models.ForeignKey('Cat_Estado', null=True, related_name='cat_estado_usuario_inscripcion')


  class Meta:
  	managed = False
  	db_table = 'registro_inscripcion'
