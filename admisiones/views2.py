# -*- coding: utf-8 -*-
from django.shortcuts import render
from admisiones.models_miutel import *
from django.contrib.auth.models import User


def por_reinscribir(request, ciclo_id):
	faltantes = Adicional.objects.raw("""
		SELECT 
			registro_adicional.id,
			registro_adicional.usuario_id, 
			registro_adicional.matricula, 
			registro_modalidad.modalidad,
			registro_licenciatura.licenciatura,
			registro_cat_estado.estado,
			estado2.estado 'estado2',
			registro_cattipoinscripcionlicenciatura.tipo_inscripcion_licenciatura,
			(SELECT COUNT(*) FROM registro_historial_academico_usuario
				JOIN grupo_grupo on grupo_grupo.id = registro_historial_academico_usuario.grupo_id
				JOIN inscripcion_periodo on inscripcion_periodo.id = grupo_grupo.idperiodo
				JOIN registro_ciclo on registro_ciclo.id = inscripcion_periodo.ciclo_id
				WHERE registro_historial_academico_usuario.usuario_id = registro_adicional.usuario_id and inscripcion_periodo.sesion = 'EQ'
				and registro_ciclo.etiqueta LIKE 'Predictamen' and registro_historial_academico_usuario.cat_estado_id in (30, 39, 40)
			) 'materias_predictamen',
			(SELECT COUNT(*) FROM registro_historial_academico_usuario
				JOIN grupo_grupo on grupo_grupo.id = registro_historial_academico_usuario.grupo_id
				JOIN inscripcion_periodo on inscripcion_periodo.id = grupo_grupo.idperiodo
				JOIN registro_ciclo on registro_ciclo.id = inscripcion_periodo.ciclo_id
				WHERE registro_historial_academico_usuario.usuario_id = registro_adicional.usuario_id and inscripcion_periodo.sesion = 'EQ'
				and registro_ciclo.etiqueta LIKE 'Dictamen' and registro_historial_academico_usuario.cat_estado_id in (30, 39, 40)
			) 'materias_dictamen',
			(SELECT COUNT(*) FROM registro_historial_academico_usuario
				JOIN grupo_grupo on grupo_grupo.id = registro_historial_academico_usuario.grupo_id
				JOIN inscripcion_periodo on inscripcion_periodo.id = grupo_grupo.idperiodo
				JOIN registro_ciclo on registro_ciclo.id = inscripcion_periodo.ciclo_id
				WHERE registro_historial_academico_usuario.usuario_id = registro_adicional.usuario_id and inscripcion_periodo.sesion <> 'EQ'
				and registro_historial_academico_usuario.cat_estado_id in (30, 39, 40)
			) 'materias_aprobadas',
			registro_cat_area_mayor.area_mayor,
			mn1.area_menor,
			mn2.area_menor
		FROM registro_inscripcion
		JOIN registro_adicional on registro_adicional.usuario_id = registro_inscripcion.usuario_id
		JOIN registro_cat_estado on registro_cat_estado.id = registro_inscripcion.cat_estado_id
		JOIN registro_cat_estado estado2 on estado2.id = registro_inscripcion.cat_estado_usuario_inscripcion_id
		JOIN registro_modalidad on registro_modalidad.id = registro_inscripcion.modalidad_id
		JOIN registro_licenciatura on registro_licenciatura.id = registro_inscripcion.licenciatura_id
		JOIN registro_cattipoinscripcionlicenciatura on registro_cattipoinscripcionlicenciatura.id = registro_inscripcion.cat_tipo_inscripcion_licenciatura_id
		LEFT JOIN registro_areas_salida_usuario on registro_areas_salida_usuario.inscripcion_id = registro_inscripcion.id
		LEFT JOIN registro_cat_area_mayor on registro_cat_area_mayor.id = registro_areas_salida_usuario.area_mayor_id
		LEFT JOIN registro_cat_area_menor mn1 on mn1.id = registro_areas_salida_usuario.area_menor_uno_id
		LEFT JOIN registro_cat_area_menor mn2 on mn2.id = registro_areas_salida_usuario.area_menor_dos_id
		WHERE registro_inscripcion.id in (SELECT DISTINCT ric.inscripcion_id FROM registro_inscripcionciclo ric
			WHERE ric.ciclo_id in ( 167, 148, 126, 101, 57, 54, 56, 53, 55, 52, 6, 5, 4, 3, 2, 1) 
			and ric.ciclo_id not in (168, 308)
			and ric.cat_estado_id in (55, 56)
		)
		and registro_inscripcion.cat_estado_id in (67, 72,73,45,71)
		and registro_inscripcion.modalidad_id = 1
		and registro_inscripcion.cat_estado_usuario_inscripcion_id in (51, 52)
		and registro_inscripcion.id not in (
			SELECT ri.id FROM registro_inscripcion ri
			JOIN registro_inscripcionciclo on ri.id = registro_inscripcionciclo.inscripcion_id
			WHERE registro_inscripcionciclo.ciclo_id = 168
			and registro_inscripcionciclo.cat_estado_id in (55, 56)
			and registro_inscripcionciclo.cat_estado_inscripcion_ciclo_id = 2
		)
		ORDER BY estado2.estado, registro_adicional.matricula
	""")
	contador = 0
	for reg in faltantes:
		contador += 1
	print contador
	return render(request, 'por_reinscribir.html', locals())


def materias_genericas(request, ciclo_id):
	materias = 'MAT%%'
	genericas = Adicional.objects.raw("""
		SELECT 
			registro_adicional.id,
			registro_adicional.matricula,
			registro_licenciatura.licenciatura,
			estado1.estado 'estado1',
			estado2.estado 'estado2',
			registro_cat_asignatura.clave_asignatura,
			registro_cat_asignatura.asignatura,
			registro_asignaturas_ciclo.inicio 'bimestre',
			registro_cat_estado.estado 'estado_materia'
		FROM registro_cat_asignatura
			JOIN registro_asignaturas_ciclo ON registro_asignaturas_ciclo.cat_asignatura_id = registro_cat_asignatura.id
			JOIN registro_historial_academico_usuario ON registro_historial_academico_usuario.asignaturas_ciclo_id = registro_asignaturas_ciclo.id
			JOIN registro_cat_estado ON registro_cat_estado.id = registro_historial_academico_usuario.cat_estado_id
			JOIN registro_adicional ON registro_adicional.usuario_id = registro_historial_academico_usuario.usuario_id
			JOIN registro_ordenhistorialacademicousuario ON registro_ordenhistorialacademicousuario.historial_academico_usuario_id = registro_historial_academico_usuario.id
			JOIN registro_inscripcionciclo ON registro_ordenhistorialacademicousuario.inscripcionciclo_id = registro_inscripcionciclo.id
			JOIN registro_inscripcion ON registro_inscripcion.id = registro_inscripcionciclo.inscripcion_id
			JOIN registro_licenciatura ON registro_licenciatura.id = registro_inscripcion.licenciatura_id
			JOIN registro_cat_estado estado1 ON estado1.id = registro_inscripcion.cat_estado_id
			JOIN registro_cat_estado estado2 ON estado2.id = registro_inscripcion.cat_estado_usuario_inscripcion_id
		WHERE 
			registro_cat_asignatura.clave_asignatura LIKE '%s' AND 
			registro_cat_estado.id IN (39, 40) AND 
			registro_asignaturas_ciclo.ciclo_id = 168
		ORDER BY registro_adicional.matricula, registro_asignaturas_ciclo.inicio
	""" %materias)
	contador = 0
	for reg in genericas:
		contador += 1
	print contador
	return render(request, 'materias_genericas.html', locals())

