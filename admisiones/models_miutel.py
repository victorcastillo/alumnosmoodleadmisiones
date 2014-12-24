# -*- coding: utf-8 -*-
#from decimal import Decimal
#import itertools
import base64, datetime

from django.db import models
from django.contrib.auth.models import User
#from django.db.models import Sum, Count, F, Q
#from django.db.models.query import QuerySet
#from django.db.models.signals import post_save
#from django.contrib.auth.models import User, Group
#from django.contrib.sites.models import Site
from django.utils.translation import ugettext as _
#from django.utils.encoding import force_unicode, smart_unicode as _su

class Adicional( models.Model ):
  usuario           = models.OneToOneField( User )
  
  matricula         = models.CharField(max_length=250, unique=True)
  
  fecha_cambio_estado = models.DateTimeField(null=True, blank=True)
  #grupo_principal   = models.ForeignKey(Group, null=True, blank=True)
  #entidad_negocio_principal = models.ForeignKey('EntidadNegocio', null=True, blank=True)
  #exportado = models.BooleanField(default=False, db_index=True)
  #password_sha1 = models.CharField(max_length=40, blank=True)
  #_password_rsa = models.TextField(db_column='password_rsa', blank=True)
  
  es_operador = models.BooleanField(default=False)
  fecha_matriculacion = models.DateTimeField(null=True, blank=True)
  #sugarid = models.CharField(max_length=36, validators=[validar_sugarid], default='', blank=True)
  
  class Meta:
    managed = False
    db_table = 'registro_adicional'
"""
  def __unicode__(self):
    return str(self.id) + ' | ' + self.usuario.email

  class Meta:
    verbose_name_plural = _('Usuarios (adicional)')

  #def obtener_documentacion_proceso_validacion(self):
    #return Documentacion_Usuario.objects.obtener_documentacion_proceso_validacion(self.usuario)

  def set_password_rsa(self, password_rsa):
    self._password_rsa = base64.encodestring(password_rsa)

  def get_password_rsa(self):
    return base64.decodestring(self._password_rsa)

  password_rsa = property(get_password_rsa, set_password_rsa)

  def desencripta_password_rsa(self):
    #from registro.views_dev1 import desencripta_rsa, generar_password_aleatorio
    #try:
      #return desencripta_rsa(self.password_rsa)
    #except Exception, e: pass

    return _(_su('Error en obtención de password.'))
"""


class Licenciatura( models.Model ):
  licenciatura = models.CharField( max_length = 250 )
  abreviatura = models.CharField(max_length=20, blank=True)
  grupo = models.CharField(max_length=50, blank=True)
  clave_plan = models.CharField(max_length=10, db_index=True)
  habilitada = models.BooleanField()
  modalidad = models.ForeignKey('Modalidad')
  asignaturas = models.ManyToManyField('Cat_Asignatura', through='Asignatura_Licenciatura')
  #objects = LicenciaturaManager()
  
  class Meta:
    managed = False
    db_table = 'registro_licenciatura'
"""
  def __unicode__(self):
    return unicode(self.licenciatura)

  def en_jornada(self):
    return self.modalidad_id in (1, 5, 6, 8)

  def aplica_reinscripcion(self):
    return self.modalidad.aplica_reinscripcion
"""


class Ciclo(models.Model):
  fecha_inicio = models.DateField()
  fecha_fin = models.DateField()
  fecha_limite_decision = models.DateField(default=None, null=True)
  clave_ciclo = models.CharField(max_length=10)
  habilitado = models.BooleanField()
  modalidad = models.ForeignKey('Modalidad', null=True)
  etiqueta = models.CharField(max_length=256)
  #objects = CicloManager()
  anio_academico = models.CharField(max_length='12', null=True, blank=True)
  periodo_academico = models.CharField(max_length='10', null=True, blank=True)
  sesion_academico = models.CharField(max_length='10', null=True, blank=True)
  
  class Meta:
    managed = False
    db_table = 'registro_ciclo'
"""
  def __unicode__(self):
    return self.clave_ciclo

  def obtener_periodos_ingreso(self, cat_estado_inscripcion_ciclo):
    return PeriodoIngreso.objects.obtener_periodos_ingreso(self, cat_estado_inscripcion_ciclo)
    #return self.periodoingreso_set.filter(
      #habilitado=True,
      #fecha_limite_inscripcion__gte=datetime.date.today(),
      #cat_estado_inscripcion_ciclo=cat_estado_inscripcion_ciclo
    #).order_by('fecha_inicio')

  def es_proximo(self):
    return self.fecha_inicio > datetime.date.today()

  #def obtener_inscripcion(self, usuario):
    #return InscripcionCiclo.objects.get(~Q(cat_estado__id__in=[57, 66]), ciclo__id=self.id, usuario=usuario)
"""


class Cat_Asignatura( models.Model ):
  asignatura = models.CharField(max_length=250)
  descripcion = models.TextField()
  cat_area_menor = models.ForeignKey('Cat_Area_Menor', null=True) #NO SE USA, se agarran los de Asignatura_Licenciatuar
  cat_area_mayor = models.ForeignKey('Cat_Area_Mayor', null=True) #NO SE USA, se agarran los de Asignatura_Licenciatuar
  clave_asignatura = models.CharField(max_length=15, db_index=True)
  #objects = CatAsignaturaManager()

  # Creados para integracion con escolares
  tipo_materia = models.ForeignKey('asignatura.TipoMateria', db_column=u'idtipomateria', null=True)
  nombrecorto = models.CharField(max_length=60, null=True)
  creditos = models.FloatField(null=True)

  class Meta:
    managed = False
    db_table = 'registro_cat_estado'
"""
  def __unicode__(self):
    return '%s | %s' % (self.clave_asignatura, self.asignatura)

  def obtener_prefijo_form(self):
    return 'cat_asignatura-%s' % self.id
"""


class Cat_Area_Mayor(models.Model):
  area_mayor = models.CharField(max_length=250)
  abreviatura = models.CharField(max_length=30)
  en_jornada = models.BooleanField(default=False)
  descripcion = models.CharField(max_length=252, default="" )
  
  class Meta:
    managed = False
    db_table = 'registro_cat_area_mayor'

class Cat_Area_Menor( models.Model ):
	area_menor = models.CharField( max_length = 250 )
	abreviatura = models.CharField( max_length = 30 )
	area_mayor = models.ForeignKey( 'Cat_Area_Mayor' )
	descripcion = models.CharField(max_length=252, default="" )
	
	class Meta:
		managed = False
		db_table = 'registro_cat_area_menor'

class Asignatura_Licenciatura( models.Model ):
  licenciatura = models.ForeignKey( 'Licenciatura' )
  cat_asignatura = models.ForeignKey( 'Cat_Asignatura' )
  cuatrimestre = models.IntegerField( max_length = 2 )
  cat_area_menor = models.ForeignKey('Cat_Area_Menor', null=True)
  cat_area_mayor = models.ForeignKey('Cat_Area_Mayor', null=True)
  oficial = models.BooleanField()
  
  class Meta:
    managed = False
    db_table = 'registro_asignatura_licenciatura'

class Asignaturas_Ciclo( models.Model ):
  cat_asignatura = models.ForeignKey('Cat_Asignatura')
  ciclo = models.ForeignKey('Ciclo')
  periodo = models.ForeignKey('Periodo', null=True)
  costo =  models.DecimalField(max_digits=14, decimal_places=2)
  habilitado = models.BooleanField()
  inicio = models.CharField(max_length=1, db_index=True)
  duracion = models.CharField(max_length=1)
  asignaturasciclo_licenciaturas = models.ManyToManyField(Licenciatura, through='AsignaturaCicloLicenciatura')
  #objects = AsignaturaCicloManager()
  
  class Meta:
    managed = False
    db_table = 'registro_asignaturas_ciclo'

  # Campos agregados para integración con sistema Escoalres

  # tipo_materia = models.ForeignKey('asignatura.TipoMateria', db_column=u'idtipomateria', null=True, default=None)
  # nombrecorto = models.CharField(max_length=60, default='')
  # creditos = models.FloatField(default=0.0)
"""
  def __unicode__(self):
    return '%s | %s | %s' % (self.cat_asignatura.asignatura, self.ciclo.clave_ciclo, self.costo)

  def obtener_asignatura_predeterminada(self, usuario):
    try:
      # la combinacion de Asignaturas_Ciclo y User es unica
      return self.asignaturaspredeterminadas_set.get(usuario=usuario)
    except AsignaturasPredeterminadas.DoesNotExist, AsignaturasPredeterminadas.MultipleObjectsReturned: pass

    return None

  def obtener_asignaturaciclo_licenciatura(self, licenciatura, periodo_ingreso):
    try:
      # la combinacion de Asignaturas_Ciclo, Licenciatura y PeriodoIngreso es unica
      return self.asignaturaciclolicenciatura_set.get(licenciatura=licenciatura, periodo_ingreso=periodo_ingreso)
    except AsignaturaCicloLicenciatura.DoesNotExist, AsignaturaCicloLicenciatura.MultipleObjectsReturned: pass

    return None

  class Meta:
    unique_together = ('cat_asignatura', 'ciclo', 'costo', 'inicio')
"""


class Areas_Salida_Usuario(models.Model):
	usuario = models.ForeignKey(User)
	inscripcion = models.ForeignKey('Inscripcion')
	area_mayor = models.ForeignKey('Cat_Area_Mayor', null = True)
	area_menor_uno = models.ForeignKey('Cat_Area_Menor', null = True, related_name = 'area_menor_uno')
	area_menor_dos = models.ForeignKey('Cat_Area_Menor', null = True, related_name = 'area_menor_dos')
	area_mayor_bloqueada = models.BooleanField(default = False)
	area_menor_uno_bloqueada = models.BooleanField(default = False)
	area_menor_dos_bloqueada = models.BooleanField(default = False)

	class Meta:
		managed = False
		db_table = 'registro_areas_salida_usuario'


class Cat_Estado(models.Model):
  ESTADOS_TRAMITE_SA = (78, 79, 80, 81, 82, 83, 84)
  ESTADO_TRAMITE_CREDENCIAL = (102, 103, 104, 105, 106, 107, 108, 109)
  BAJA_DEFINITIVA = 94
  PROSPECTO = 50

  estado = models.CharField(max_length=100)
  contexto = models.CharField(max_length=100)
  #objects = CatEstadoManager()
  #estados_doc_usuario = EstadosDocumentacionUsuarioManager()
  #estados_orden = EstadosOrdenManager()
  #estados_inscripcion = EstadosInscripcionManager()
  #estados_usuario = EstadosUsuarioManager()
  #estados_hau = EstadosHAUManager()
  
  class Meta:
    managed = False
    db_table = 'registro_cat_estado'
"""
  def __unicode__(self):
    return self.estado + ' | ' + self.contexto

  def es_estado_matriculado(self):
    return esta_matriculado(None, self)

  class Meta:
    verbose_name = _('Cat. estado')
    verbose_name_plural = _('Cat. estados usuario')
    ordering = ['contexto']
"""


class Inscripcion(models.Model):
  ACTIVA = 45
  SA_POR_LLENAR = 89
  SA_POR_ENVIAR = 90
  SA_POR_VALIDAR = 91
  SELECC_CARGA_ACADEMICA = 92
  MATRICULADO = 67
  CAMBIO_CARRERA = 101
  PROGRAMA_CONCLUIDO = 93
  EGRESADO = 120
  CAMBIO_CICLO = 123
  CAT_ESTADO_VALIDOS = (24, 26, ACTIVA, MATRICULADO, 71, 72, 73, SA_POR_LLENAR, SA_POR_ENVIAR, SA_POR_VALIDAR, SELECC_CARGA_ACADEMICA)
  INSCRIPCIONES_NO_PUEDE_MOSTRAR_INTERFAZ = (15, SA_POR_LLENAR, SA_POR_ENVIAR, SA_POR_VALIDAR, 96, 97, 98)
  INSCRIPCIONES_PENDIENTES = (15, SA_POR_LLENAR, SA_POR_ENVIAR, SA_POR_VALIDAR, SELECC_CARGA_ACADEMICA, 96, 97, 98)
  INSCRIPCIONES_NO_ACTIVAS = (15, PROGRAMA_CONCLUIDO, 97, 98, CAMBIO_CARRERA)
  INSCRIPCIONES_NO_PUEDE_MOSTRAR_MODALIDADES_INSCRITAS = (15, 97, 98)
  INSCRIPCIONES_CANCELADAS = (97, 98)
  INSCRIPCIONES_NO_CONSIDERAR_DOCS = (15, 97, 98, CAMBIO_CARRERA)
  CAT_ESTADO_INSCRIPCION_CONCLUIDA = (96, 97, 98)
  ESTADOS_INSCRIPCION_DOCUMENTOS = (SA_POR_VALIDAR, SELECC_CARGA_ACADEMICA, 24, 25, 26, 28, ACTIVA, MATRICULADO, 69, 71, 72, 73)
  INSCRIPCIONES_PUEDEN_INICIAR_NVAMENTE = (97, 98, CAMBIO_CARRERA, PROGRAMA_CONCLUIDO, EGRESADO, CAMBIO_CICLO)

  STATUS = {
    'solicitud_por_llenar': 89,
    'solicitud_por_enviar': 90,
    'solicitud_por_validar': 91,
    'seleccionar_carga_academica': 92,
    'solicitud_regresada': 96,
    'solicitud_rechazada': 97,
    'inscripcion_inactiva': 15,
    'inscripcion_en_proceso': 24,
    'inscripcion_con_doctos': 25,
    'inscripcion_exitosa': 26,
    'inscripcion_anulada': 27,
    'inscripcion_baja_temporal': 28,
    'inscripcion_baja_definitiva': 29,
    'inscripcion_activa': 45,
    'matriculado': 67,
    'inactivo': 68,
    'pendiente_baja': 69,
    'baja_por_reglamento': 70,
    'nuevo_ingreso': 71,
    'pendiente_reinscripcion': 72,
    'posible_reingreso': 73,
    'programa_concluido': 93,
    'solicitud_cancelada': 98,
    'pendiente_baja_definitiva': 99,
    'cancelacion_de_venta': 100,
    'cambio_de_carrera': 101,
    'egresado': 120,
    'cambio_de_ciclo': 123
  }

  modalidad = models.ForeignKey('Modalidad', null=True)
  usuario = models.ForeignKey(User)
  alta =  models.DateField(auto_now_add=True)
  cat_estado = models.ForeignKey(Cat_Estado, verbose_name=_('Estado'))
  ciclo = models.ForeignKey('Ciclo', null=True, blank=True)
  periodo_ingreso = models.ForeignKey('PeriodoIngreso', null=True, blank=True)
  licenciatura = models.ForeignKey(Licenciatura, null=True)
  # no se utiliza. Ahora esta en Tramite
  contrato_aceptado = models.BooleanField(default=False)
  # no se utiliza. Ahora esta en Tramite
  fecha_contrato = models.DateTimeField(auto_now_add=True)
  documentacion = models.BooleanField()
  cat_tipo_inscripcion_licenciatura = models.ForeignKey('CatTipoInscripcionLicenciatura', null=True, blank=True)
  solicitud_admision = models.OneToOneField('tramites.Tramite', null=True, blank=True)
  fecha_enrolamiento = models.DateTimeField(null=True, blank=True)
  cat_estado_usuario_inscripcion = models.ForeignKey(Cat_Estado, null=True, related_name='cat_estado_usuario_inscripcion')
  exportado_moodle = models.BooleanField(default=False)
  #objects = InscripcionManager()

  #def __unicode__(self):
    #if self.licenciatura:
      #return self.licenciatura.licenciatura + ' | ' + self.cat_estado.estado
#
    #return self.cat_estado.estado
  class Meta:
    managed = False
    db_table = 'registro_inscripcion'
"""
  def es_valida(self):
    return self.cat_estado_id in self.CAT_ESTADO_VALIDOS

  def obtener_ultima_inscripcionciclo(self, select_related=('cat_estado', 'ciclo', 'orden', 'periodo_ingreso')):
    inscripcionciclo_actual_proxima = InscripcionCiclo.objects.obtener_inscripcionciclo_actual_proxima(self.usuario,
      self, ordenar_por=('-ciclo__fecha_inicio',), select_related=select_related)
    if len(inscripcionciclo_actual_proxima):
      return inscripcionciclo_actual_proxima[0]
    return None

  def obtener_inscripcionesciclo_habilitadas(self, order_by=('-ciclo__fecha_inicio',), select_related=('ciclo', 'periodo_ingreso')):
    #return self.usuario.obtener_ciclos_inscritos(self, select_related=select_related, ordenar_por=order_by)
    return InscripcionCiclo.objects.obtener_ciclos_inscritos(self.usuario, self, select_related=select_related, ordenar_por=order_by)

  def obtener_inscripcionesciclo_actual_proxima(self, **kwargs):
    return InscripcionCiclo.objects.obtener_inscripcionciclo_actual_proxima(self.usuario, self, **kwargs)

  def esta_aceptada_por_alumno(self):
    return self.solicitud_admision and self.solicitud_admision.sa_aceptada()

  def es_de_alumno_nuevo_ingreso(self):
    return self.usuario.es_nuevo_ingreso(self)

  def tiene_documentacion(self):
    #return self.usuario.obtener_documentacion(self)
    return Documentacion.objects.obtener_documentacion(self.usuario_id, self)

  def obtener_ciclos_inscritos(self):
    from dashboard.views import obtener_ciclos_inscritos
    return obtener_ciclos_inscritos(self.usuario, self)

  def puede_inscribirse(self):
    try:
      return self.usuario.puede_inscribirse(self)
    except Exception, e: pass
    return False

  def puede_ver_historial_academico(self):
    return not self.cat_estado_id in self.INSCRIPCIONES_PENDIENTES

  def usuario_matriculado(self):
    return self.usuario.esta_matriculado(self)

  def usuario_admitido(self):
    return self.usuario.es_admitido(self)

  def usuario_alumno(self):
    return self.usuario.es_alumno(self)

  def obtener_ultima_cfg_reinscripcion(self):
    from perfiles.models import Cfg_Reinscripcion
    from perfiles.views2 import obtener_ultima_ic_activa
    ic =  obtener_ultima_ic_activa(self)
    if not ic:
      return None
    ciclo = ic.ciclo
    cfg_reinscripcion = Cfg_Reinscripcion.objects.filter(inscripcion=self, habilitado=True,
                                                          esta_reinscrito=False, ciclo_anterior=ciclo).order_by("-id")
    if cfg_reinscripcion:
      return cfg_reinscripcion[0]
    return None

  class Meta:
    verbose_name_plural = _('Inscripciones')
"""


class InscripcionCiclo(models.Model):
  INSCRIPCIONCICLO_CANCELADA = 57
  INSCRIPCIONCICLO_INACTIVA = 66
  PAGADO = 56
  PENDIENTE_PAGO = 55

  inscripcion = models.ForeignKey(Inscripcion)
  ciclo = models.ForeignKey('Ciclo')
  orden = models.ForeignKey('Orden', null=True)
  fecha_registro = models.DateTimeField(auto_now_add=True)
  cat_estado = models.ForeignKey('Cat_Estado')
  cat_estado_inscripcion_ciclo = models.ForeignKey('CatEstadoInscripcionCiclo')
  usuario = models.ForeignKey(User)
  periodo_ingreso = models.ForeignKey('PeriodoIngreso', null=True)
  jornada = models.ForeignKey('Jornada', null=True)
  # True si el número de materias coincide con el intervalo permitido por la jornada
  asignaturas_asignadas = models.BooleanField(default=False)
  # registro de inscripcionciclo origen en caso de cancelaciones
  origen = models.OneToOneField('self', null=True)
  #objects = InscripcionCicloManager()
  #habilitadas = InscripcionCicloHabilitadasManager()
  
  class Meta:
    managed = False
    db_table = 'registro_inscripcionciclo'
"""
  def __init__(self, *args, **kwargs):
    super(InscripcionCiclo, self).__init__(*args, **kwargs)
    self.asignaturas_cache = None

  def __unicode__(self):
    return '%s | %s | %s' % (self.id, self.ciclo.clave_ciclo, self.cat_estado_inscripcion_ciclo.estado)

  def es_reinscripcion(self):
    return self.cat_estado_inscripcion_ciclo_id == 2

  def tiene_pagos_pendientes(self):
    return self.orden_id is not None and self.cat_estado_id in (55,)

  def tiene_grupo(self):
    return self.ordenhistorialacademicousuario_set.filter(historial_academico_usuario__grupo__isnull=False).\
      exclude(historial_academico_usuario__cat_estado__in=(32, Cat_Estado.BAJA_DEFINITIVA)).count() > 0

  def obtener_asignaturas(self, order_by=('ordenhistorialacademicousuario__inscripcionciclo__periodo_ingreso__periodobimestre__fecha_inicio', 'asignaturas_ciclo__inicio')):
    #return Historial_Academico_Usuario.objects.obtener_asignaturas_orden(self.orden_id, usuario_id=self.usuario_id,
    self.asignaturas_cache = Historial_Academico_Usuario.objects.obtener_asignaturas(self, usuario_id=self.usuario_id,
      select_related=('cat_asignatura', 'asignaturas_ciclo', 'calificacion', 'grupo'),
      #order_by=('ordenhistorialacademicousuario__orden__inscripcionciclo__periodo_ingreso__periodobimestre__fecha_inicio', 'asignaturas_ciclo__inicio')
      order_by=order_by
    ).annotate(Count('id'))

    return self.asignaturas_cache

  def puede_agregar_asignatura(self):
     

      if not self.jornada_id:
        return False

      historial_academico = self.obtener_asignaturas()

      # se contaran las que tengan estado diferente de "Dada de baja" y
      # "Dada de baja definitiva"
      num_asignaturas = historial_academico.exclude(
        cat_estado__id__in=[32, Cat_Estado.BAJA_DEFINITIVA]
      ).count()
      max_jornada = self.jornada.num_max_materias + 2

      return num_asignaturas < max_jornada
      #if num_asignaturas < self.jornada.num_max_materias:
        #return True
      #return False

  def obtener_costo_total(self, **kwargs):
    if self.asignaturas_cache is None:
      self.obtener_asignaturas(**kwargs)

    return reduce(lambda costo, hau: costo + hau.asignaturas_ciclo.costo,
      filter(
        lambda hau: hau.asignaturas_ciclo.habilitado,
        self.asignaturas_cache
      ),
    0)

    #costo_total_dict = self.asignaturas_cache.filter(asignaturas_ciclo__habilitado=True
      #).aggregate(costo_total=Sum('asignaturas_ciclo__costo'))
    #return costo_total_dict['costo_total']

  def obtener_bimestres(self):
    periodo_ingreso = self.periodo_ingreso
    bimestres = []
    if periodo_ingreso:
      periodos_bimestre = periodo_ingreso.periodobimestre_set.all()
    else:
      periodos_bimestre = PeriodoBimestre.objects.none()
      ciclo = self.ciclo
      ciclo.__class__ = Ciclo
      for periodo_ingreso in ciclo.periodoingreso_set.all():
        periodos_bimestre |= periodo_ingreso.periodobimestre_set.all()

    bimestres = list(set([pb.inicio for pb in periodos_bimestre]))
    if not bimestres and ciclo.sesion_academico == "EQ":
      bimestres = ["1"]
    return bimestres
"""


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
  contrato = models.TextField()
  matricula_requerida = models.BooleanField(default=True)
  nomenclatura_periodo = models.CharField(max_length=256)
  aplica_reinscripcion = models.BooleanField(default=False)
  permite_autoinscripcion = models.BooleanField(default=False)
  clave_power_campus = models.CharField(max_length=10, null=True, blank=True)
  long_referencia = models.IntegerField()
  permite_autoreinscripcion = models.BooleanField(default=False)
  #sites = models.ManyToManyField(Site, through='ModalidadSite')
  metodos_pago = models.ManyToManyField('MetodoPago', through='ModalidadesMetodosPago')
  hay_periodo_ingreso = models.BooleanField(default=False)
  aplica_credencial = models.BooleanField(default=False)
  #objects = ModalidadManager()
  
  class Meta:
    managed = False
    db_table = 'registro_modalidad'
"""
  def __unicode__(self):
    return unicode(self.modalidad)

  def obtener_programas(self, ordenar_por=('licenciatura',)):
    return self.licenciatura_set.all().order_by(*ordenar_por)

  def obtener_cuentas_banco(self):
    return obtener_cuentas_banco(self)

  def obtener_metodos_pago(self):
    return self.metodos_pago.filter(habilitado=True).order_by('orden_interfaz')

  def puede_inscribir_mas_de_un_programa(self):
    return self.pk in (self.MOD_EC_DIPLOMADO, self.MOD_EC_CURSO, self.MOD_EC_CERTIFICACION)
"""


class Calificacion(models.Model):
    CALIFICACIONES_NO_APROBATORIAS = (u'NA', u'NP', u'5')

    etiqueta = models.CharField(unique=True, max_length=12, blank=True)
    texto = models.CharField(max_length=90, blank=True)
    numerico = models.IntegerField(null=True, blank=True)
    limiteinferior = models.FloatField(null=True, blank=True)
    limitesuperior = models.FloatField(null=True, blank=True)
    cuentapromedio = models.IntegerField()
    cuentaavance = models.IntegerField()
    
    class Meta:
		managed = False
		db_table = 'inscripcion_calificacion'
		

class Historial_Academico_Usuario(models.Model):
  BAJAS = (32, Cat_Estado.BAJA_DEFINITIVA,)

  asignaturas_ciclo = models.ForeignKey( 'Asignaturas_Ciclo' )
  cat_asignatura = models.ForeignKey( 'Cat_Asignatura' )
  usuario = models.ForeignKey( User )
  cat_estado = models.ForeignKey( 'Cat_Estado' )
  creacion = models.DateTimeField(auto_now_add=True, null=True, default=datetime.date.today())
  actualizacion = models.DateTimeField(auto_now=True)
  #objects = HistorialAcademicoUsuarioManager()

  ### Necesarios para integracion con escolaras
  grupo = models.ForeignKey('grupo.Grupo', null=True, blank=True)
  calificacion = models.ForeignKey('inscripcion.Calificacion', null=True, db_column='idcalificacion', blank=True)
  
  class Meta:
    managed = False
    db_table = 'registro_historial_academico_usuario'
"""
  def obtener_inscripcionmateria(self):
    from inscripcion.models import InscripcionMateria
    h = self
    h.__class__ = InscripcionMateria
    return h
    
  def puede_actualizar_cat_estado(self):
      if not self.cat_estado_id:
          return True

      # Dada de baja, pendiente, en curso, pueden cambiar estado
      #if self.cat_estado.id in [32,39,40]:
          #return True
      #return False
      return self.cat_estado_id in [32, 39, 40]

  def __unicode__(self):
    return '%s | %s' % (self.id, self.creacion)

  class Meta:
    verbose_name = _('Historial')
    verbose_name_plural = _('Historial academico')
"""


class CatTipoInscripcionLicenciatura(models.Model):
  tipo_inscripcion_licenciatura = models.CharField(max_length=30, blank=True)
  descripcion = models.TextField()
  mas_informacion = models.TextField()
  modalidad = models.ForeignKey('Modalidad')
  #objects = CatTipoInscripcionLicenciaturaManager()
  
  class Meta:
    managed = False
    db_table = 'registro_cattipoinscripcionlicenciatura'
"""
  def __unicode__(self):
    return '%s | %s' % (self.tipo_inscripcion_licenciatura, self.modalidad.modalidad)

  def como_html(self):
    from registro.forms_dev1 import CatTipoInscripcionLicenciaturaModelChoiceField
    model_choice_field = CatTipoInscripcionLicenciaturaModelChoiceField(queryset=self.__class__.objects.none)
    return model_choice_field.label_from_instance(self)

  class Meta:
    verbose_name = _('Tipo ingreso')
"""


class Orden( models.Model ):
  fecha = models.DateTimeField(auto_now_add=True, db_index=True)
  usuario = models.ForeignKey(User, related_name='orden')
  #operador = models.ForeignKey(User, related_name='ooperador', null=True, blank=True)
  total = models.DecimalField(max_digits=14, decimal_places=2)
  total_bruto = models.DecimalField(max_digits=14, decimal_places=2)
  cat_estado = models.ForeignKey('Cat_Estado', verbose_name=_('Estado'))
  #opcion_pago = models.ForeignKey('Opcion_Pago', verbose_name=_(force_unicode('Opción de pago')))
  informacion_adicional = models.TextField(blank=True)
  fecha_venta = models.DateField(null=True, blank=True)
  #referencias = models.ManyToManyField('Referencia', blank=True)
  #grupo_operador = models.ForeignKey(Group, null=True, blank=True)
  #entidad_negocio = models.ForeignKey('EntidadNegocio', null=True, blank=True)
  
  class Meta:
    managed = False
    db_table = 'registro_orden'


class OrdenHistorialAcademicoUsuario(models.Model):
  orden = models.ForeignKey(Orden, null=True) # en desuso
  inscripcionciclo = models.ForeignKey(InscripcionCiclo, null=True) # TODO: no deben permitirse nulos
  historial_academico_usuario = models.ForeignKey(Historial_Academico_Usuario)
  informacion_adicional = models.TextField() # deprecated
  #nota_orden = models.ForeignKey(NotaOrden, null=True) # deprecated
  fecha_creacion = models.DateTimeField(auto_now_add=True)
  fecha_actualizacion = models.DateTimeField(auto_now_add=True, auto_now=True)
  
  class Meta:
    managed = False
    db_table = 'registro_ordenhistorialacademicousuario'
"""
  class Meta:
    unique_together = ('inscripcionciclo', 'historial_academico_usuario')
    #unique_together = ('orden', 'historial_academico_usuario')
"""


class Jornada(models.Model):
  #producto_servicio = models.ForeignKey(ProductoServicio, null=True)
  porcentaje_descuento_max = models.DecimalField(max_digits=11, decimal_places=8)
  habilitado = models.BooleanField()
  num_max_materias = models.IntegerField()
  num_min_materias = models.IntegerField()
  modalidad = models.ForeignKey(Modalidad)
  periodos_ingreso = models.ManyToManyField('PeriodoIngreso')
  #ciclos = models.ManyToManyField(Ciclo)
  #objects = JornadaManager()
  
  class Meta:
    managed = False
    db_table = 'registro_jornada'
"""
  def __unicode__(self):
    return self.producto_servicio.descripcion
"""


class AsignaturaCicloLicenciatura(models.Model):
  asignatura_ciclo = models.ForeignKey(Asignaturas_Ciclo)
  licenciatura = models.ForeignKey(Licenciatura)
  periodo_ingreso = models.ForeignKey('PeriodoIngreso', null=True) # Quitar este NULL, solo por cuestion de migracion
  prioridad = models.SmallIntegerField(default=0)
  opcional = models.BooleanField(default=False)
  
  class Meta:
    managed = False
    db_table = 'registro_asignaturaciclolicenciatura'
"""
  class Meta:
    unique_together = ('asignatura_ciclo', 'licenciatura', 'periodo_ingreso')
"""


class PeriodoIngreso(models.Model):
  ciclo = models.ForeignKey(Ciclo)
  fecha_inicio = models.DateField()
  fecha_fin = models.DateField()
  fecha_limite_inscripcion = models.DateField()
  habilitado = models.BooleanField(default=True)
  etiqueta = models.CharField(max_length=256)
  descripcion = models.CharField(max_length=256)
  cat_estado_inscripcion_ciclo = models.ForeignKey('CatEstadoInscripcionCiclo')
  #objects = PeriodoIngresoManager()
  
  class Meta:
    managed = False
    db_table = 'registro_periodoingreso'
"""
  def obtener_periodoingreso_bim(self, inicio):
    try:
      return self.periodobimestre_set.get(inicio=inicio, habilitado=True)
    except (PeriodoBimestre.DoesNotExist, PeriodoBimestre.MultipleObjectsReturned): pass

    return None

  def __unicode__(self):
    return '%s - %s' % (self.ciclo_id, self.fecha_inicio)
"""


class PeriodoBimestre(models.Model):
  periodo_ingreso = models.ForeignKey('PeriodoIngreso')
  inicio = models.CharField(max_length=1)
  fecha_inicio = models.DateField()
  fecha_fin = models.DateField()
  habilitado = models.BooleanField(default=True)
  
  class Meta:
    managed = False
    db_table = 'registro_periodobimestre'
"""
  class Meta:
    unique_together = ('periodo_ingreso', 'inicio')
"""



