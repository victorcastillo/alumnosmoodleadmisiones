from django.shortcuts import render
from admisiones.models import *
from moodle.models import *
from django.contrib.auth.models import User





def home(request):

	alumnos_moodle = set([str(x).strip() for x in UserRoleA.objects.filter(role__id__in=[5,16], user__deleted=0,user__suspended=0)\
		.select_related('user').order_by('user__username').values_list('user__username', flat=True)])
	alumnos_admisiones_set = set([str(x) for x in Inscripcion.objects.filter(cat_estado_usuario_inscripcion__id__in=[51,52], modalidad__id__in=[1,6,7,2,3,4,8]).\
		order_by('usuario__adicional__matricula').values_list('usuario__adicional__matricula', flat=True)])

	#Admisiones vs Moodle
	coinciden_en_ambos = alumnos_admisiones_set & alumnos_moodle
	admisiones_no_estan_en_moodle = alumnos_admisiones_set-coinciden_en_ambos
	cuenta_admisiones_no_estan_en_moodle = len(list(alumnos_admisiones_set-coinciden_en_ambos))
	cuenta_coinciden_en_ambos = len(list(coinciden_en_ambos))
	
	##Moodle vs Admisiones
	coinciden_en_ambos_moodle = alumnos_moodle & alumnos_admisiones_set
	moodle_no_estan_en_admisiones = alumnos_moodle-coinciden_en_ambos_moodle
	cuenta_moodle_no_estan_en_admisiones = len(list(alumnos_moodle-coinciden_en_ambos_moodle))
	cuenta_coinciden_en_ambos_moodle = len(list(coinciden_en_ambos_moodle))
	return render(request, 'index.html', locals())


def home_2(request):

	alumnos_moodle = set([str(x).strip() for x in UserRoleA.objects.filter(role__id__in=[5,16], user__deleted=0,user__suspended=0)\
		.select_related('user').order_by('user__username').values_list('user__username', flat=True) if x])
	alumnos_admisiones_set = set([str(x).strip() for x in User.objects.all().values_list('adicional__matricula', flat=True) if x])

	#Admisiones vs Moodle
	coinciden_en_ambos = alumnos_admisiones_set & alumnos_moodle
	admisiones_no_estan_en_moodle = alumnos_admisiones_set-coinciden_en_ambos
	cuenta_admisiones_no_estan_en_moodle = len(list(alumnos_admisiones_set-coinciden_en_ambos))
	cuenta_coinciden_en_ambos = len(list(coinciden_en_ambos))
	
	##Moodle vs Admisiones
	coinciden_en_ambos_moodle = alumnos_moodle & alumnos_admisiones_set
	moodle_no_estan_en_admisiones = alumnos_moodle-coinciden_en_ambos_moodle
	cuenta_moodle_no_estan_en_admisiones = len(list(alumnos_moodle-coinciden_en_ambos_moodle))
	cuenta_coinciden_en_ambos_moodle = len(list(coinciden_en_ambos_moodle))
	return render(request, 'index.html', locals())


def por_ciclo(request,ciclo_id,categoria_id):


	alumnos_moodle = UserRoleA.objects.raw("""
				select distinct
				u.username as id
				from mdl_user u
				join mdl_user_enrolments ue on ue.userid = u.id
				join mdl_enrol e on e.id = ue.enrolid
				join mdl_role_assignments ra on ra.userid = u.id
				join mdl_context ct on ct.id = ra.contextid and ct.contextlevel = 50
				join mdl_course c on c.id = ct.instanceid and e.courseid = c.id
				join mdl_role r on r.id = ra.roleid and r.id in (5,16)
				where
				e.status = 0
				and u.suspended = 0
				and u.deleted = 0
				and (ue.timeend = 0 or ue.timeend > now())
				and c.category = %d
				order by u.username
	""" % int(categoria_id))

 	print """
				select distinct
				u.username as id
				from mdl_user u
				join mdl_user_enrolments ue on ue.userid = u.id
				join mdl_enrol e on e.id = ue.enrolid
				join mdl_role_assignments ra on ra.userid = u.id
				join mdl_context ct on ct.id = ra.contextid and ct.contextlevel = 50
				join mdl_course c on c.id = ct.instanceid and e.courseid = c.id
				join mdl_role r on r.id = ra.roleid and r.id in (5,16)
				where
				e.status = 0
				and u.suspended = 0
				and u.deleted = 0
				and (ue.timeend = 0 or ue.timeend > now())
				and c.category = %d
				order by u.username
	""" % int(categoria_id)
	ciclo = Ciclo.objects.get(id=ciclo_id)
	alumnos_moodle = set((x.id for x in alumnos_moodle))

	alumnos_admisiones_set = set(InscripcionCiclo.objects.filter(ciclo=int(ciclo_id), inscripcion__cat_estado_usuario_inscripcion__id__in=[51,52]).\
	exclude(cat_estado__id__in=[InscripcionCiclo.INSCRIPCIONCICLO_CANCELADA, InscripcionCiclo.INSCRIPCIONCICLO_INACTIVA]).\
	order_by('inscripcion__usuario__adicional__matricula').values_list('inscripcion__usuario__adicional__matricula', flat=True))

	#Admisiones vs Moodle
	coinciden_en_ambos = alumnos_admisiones_set & alumnos_moodle
	admisiones_no_estan_en_moodle = alumnos_admisiones_set-coinciden_en_ambos
	cuenta_admisiones_no_estan_en_moodle = len(list(alumnos_admisiones_set-coinciden_en_ambos))
	cuenta_coinciden_en_ambos = len(list(coinciden_en_ambos))

	#Moodle vs Admisiones
	
	coinciden_en_ambos_moodle = alumnos_moodle & alumnos_admisiones_set
	moodle_no_estan_en_admisiones = alumnos_moodle-coinciden_en_ambos_moodle
	cuenta_moodle_no_estan_en_admisiones = len(list(alumnos_moodle-coinciden_en_ambos_moodle))
	cuenta_coinciden_en_ambos_moodle = len(list(coinciden_en_ambos_moodle))

	return render(request, 'por_ciclo.html', locals())
