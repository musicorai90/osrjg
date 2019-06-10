#-*- coding: utf-8 -*-
from __future__ import print_function

from io import BytesIO
import django
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib import auth, messages
from django.utils import timezone
from PIL import Image
from xhtml2pdf import pisa
import cStringIO as StringIO
from django.template.loader import get_template
from django.template import Context
import random
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django import http
import json

registro = False
cedExist = False
adminsNum = len(Admin.objects.all())

def login(request):
	if request.user.is_authenticated:
		return redirect('index')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password = request.POST.get('password')
			user = auth.authenticate(username=username,password=password)
			if user is not None:
				#usuario = auth.models.User.objects.get(username=username)
				try:
					user.groups.get()
					auth.login(request,user)
					return redirect('index')
				except:
					messages.error(request, 'Verifique su usuario y contraseña.')
			else:
				messages.error(request, 'Verifique su usuario y contraseña.')

		return render(request, 'Orquesta/login.html')

@login_required
def logout(request):
	auth.logout(request)
	return redirect('login')

@login_required
def index(request):
	global registro
	evaluaciones = []
	evaAll = Evaluacion.objects.all()
	if str(request.user.groups.get()) == 'admin':
		solicitudes = Solicitud.objects.all().order_by('id').reverse()
		usuario = Admin.objects.get(cedula=request.user.username)
		contexto = {'tipo': 'admin','solicitudes': solicitudes,'usuario': usuario}
		if registro:
			registro = False
		return render(request, 'Orquesta/index_admin.html',contexto)
	elif str(request.user.groups.get()) == 'profesor':
		usuario = Profesor.objects.get(cedula=request.user.username)
		for evaluacion in evaAll:
			if str(evaluacion.alumno.instrumento.profesor.id) == str(usuario.id):
				evaluaciones.append(evaluacion)
		contexto = {'tipo': 'profesor','evaluaciones': evaluaciones,'usuario': usuario}
		if registro:
			registro = False
		return render(request, 'Orquesta/index_profe.html',contexto)
	elif str(request.user.groups.get()) == 'alumno':
		usuario = Alumno.objects.get(cedula=request.user.username)
		evaAll = Evaluacion.objects.all()
		for evaluacion in evaAll:
			if str(evaluacion.alumno.id) == str(usuario.id):
				evaluaciones.append(evaluacion)
		contexto = {'tipo': 'alumno','evaluaciones': evaluaciones,'usuario': usuario}
		if registro:
			registro = False
		return render(request, 'Orquesta/index_alumno.html',contexto)

@login_required
def perfil(request):
	global registro
	if str(request.user.groups.get()) == 'admin':
		usuario = Admin.objects.get(cedula=request.user.username)
	elif str(request.user.groups.get()) == 'profesor':
		usuario = Profesor.objects.get(cedula=request.user.username)
	elif str(request.user.groups.get()) == 'alumno':
		usuario = Alumno.objects.get(cedula=request.user.username)
	contexto = {'tipo': str(request.user.groups.get()),'usuario': usuario,'registro':registro}
	if registro:
		registro = False
	return render(request,'Orquesta/perfil.html',contexto)

@login_required
def modificarPerfil(request):
	global registro
	if str(request.user.groups.get()) == 'admin':
		usuario = Admin.objects.get(cedula=request.user.username)
		instance = get_object_or_404(Admin,id=usuario.id)
		form = AdminForm(request.POST or None, instance=instance)
	elif str(request.user.groups.get()) == 'profesor':
		usuario = Profesor.objects.get(cedula=request.user.username)
		instance = get_object_or_404(Profesor,id=usuario.id)
		form = ProfesorForm(request.POST or None, instance=instance)
	elif str(request.user.groups.get()) == 'alumno':
		usuario = Alumno.objects.get(cedula=request.user.username)
		instance = get_object_or_404(Alumno,id=usuario.id)
		form = AlumnoForm(request.POST or None, instance=instance)
	if form.is_valid():
		form.save()
		registro = True
		return redirect('perfil')
	contexto = {'tipo': str(request.user.groups.get()),'usuario': usuario,'form': form,'registro':registro,'cambiar': False}
	return render(request,'Orquesta/modificar_perfil.html',contexto)

@login_required
def cambiarImagen(request):
	global registro
	if str(request.user.groups.get()) != '':
		if str(request.user.groups.get()) == 'admin':
			usuario = Admin.objects.get(cedula=request.user.username)
		elif str(request.user.groups.get()) == 'profesor':
			usuario = Profesor.objects.get(cedula=request.user.username)
		elif str(request.user.groups.get()) == 'alumno':
			usuario = Alumno.objects.get(cedula=request.user.username)
		if request.method == 'POST' and request.FILES['image']:
			usuario.foto = request.FILES['image']
			usuario.save()
			image = Image.open(usuario.foto)
			tamanio = image.size
			if tamanio[0] > tamanio[1]:
				pos = (tamanio[0] - tamanio[1]) / 2
				newImage = image.crop((pos,0,tamanio[1]+pos,tamanio[1]))
			elif tamanio[0] < tamanio[1]:
				pos = (tamanio[1] - tamanio[0]) / 2
				newImage = image.crop((0,pos,tamanio[0],tamanio[0]+pos))
			else:
				newImage = image.crop((0,0,tamanio[0],tamanio[0]))
			newImage.save("media/fotos/%s" %request.FILES['image'])
			registro = True
			return redirect('index')
		contexto = {'tipo': str(request.user.groups.get()),'usuario': usuario}
		return render(request, 'Orquesta/cambiarImagen.html',contexto)
	else:
		return redirect('logout')

@login_required
def contrasena(request):
	global registro
	if str(request.user.groups.get()) == 'admin':
		usuario = Admin.objects.get(cedula=request.user.username)
	elif str(request.user.groups.get()) == 'profesor':
		usuario = Profesor.objects.get(cedula=request.user.username)
	elif str(request.user.groups.get()) == 'alumno':
		usuario = Alumno.objects.get(cedula=request.user.username)
	if request.method == 'POST':
		contrasena = request.POST.get('contrasena')
		if contrasena is not None:
			user = auth.models.User.objects.get(username=usuario.cedula)
			user.set_password(contrasena)
			user.save()
			registro = True
			return redirect('index')
	return render(request, 'Orquesta/contrasena.html', {'tipo': str(request.user.groups.get()), 'usuario': usuario})

@login_required
def admins(request):
	global registro
	if str(request.user.groups.get()) == 'admin':
		admins = Admin.objects.all()
		usuario = Admin.objects.get(cedula=request.user.username)
		contexto = {'tipo': str(request.user.groups.get()),'admins': admins,'registro': registro,'usuario': usuario,'cantidad': len(admins)}
		if registro:
			registro = False
		return render(request, 'Orquesta/admins.html',contexto)
	elif str(request.user.groups.get()) != 'admin' and str(request.user.groups.get()) != '':
		return redirect('index')

@login_required
def agregar_admin(request):
	global registro
	global cedExist
	if adminsNum > 2:
		return redirect('index')
	elif str(request.user.groups.get()) == 'admin':
		usuario = Admin.objects.get(cedula=request.user.username)
		cedExist = False
		if request.method == 'POST':
			form = AdminForm(request.POST)
			if form.is_valid():
				existe = False
				admins = Admin.objects.all()
				alumnos = Alumno.objects.all()
				profesores = Profesor.objects.all()
				cedula = request.POST.get('cedula')
				for admin in admins:
					if str(admin.cedula) == str(cedula):
						existe = True
				for profesor in profesores:
					if str(profesor.cedula) == str(cedula):
						existe = True
				for alumno in alumnos:
					if str(alumno.cedula) == str(cedula):
						if not alumno.fecha_egr:
							existe = True
				if existe:
					cedExist = True
				else:
					user = auth.models.User.objects.create_user(cedula,'',cedula)
					user.groups.set('1')
					form.save()
					registro = True
					return redirect('admins')
		else:
			form = AdminForm()

		return render(request, 'Orquesta/nuevo_admin.html', {'form': form,'cedExist':cedExist,'tipo': str(request.user.groups.get()), 'usuario': usuario})
	else:
		return redirect('index')

@login_required
def perfilAdmin(request, admin_id):
	if str(request.user.groups.get()) == 'admin':
		usuario = Admin.objects.get(cedula=request.user.username)
		if str(admin_id) == str(usuario.cedula):
			return redirect('perfil')
		else:
			admin = get_object_or_404(Admin,cedula=admin_id)
			contexto = {'tipo': str(request.user.groups.get()),'usuario': usuario,'admin':admin}
			return render(request,'Orquesta/admin.html',contexto)
	else:
		return redirect('index')

@login_required
def cambiarAdmin(request):
	global registro
	global cedExist
	if str(request.user.groups.get()) == 'admin':
		cedExist = False
		usuario = Admin.objects.get(cedula=request.user.username)
		instance = get_object_or_404(Admin,id=usuario.id)
		form = AdminForm(request.POST or None, instance=instance)
		if form.is_valid():
			existe = False
			admins = Admin.objects.all()
			alumnos = Alumno.objects.all()
			profesores = Profesor.objects.all()
			cedula = request.POST.get('cedula')
			for admin in admins:
				if str(admin.cedula) == str(cedula):
					existe = True
			for profesor in profesores:
				if str(profesor.cedula) == str(cedula):
					existe = True
			for alumno in alumnos:
				if str(alumno.cedula) == str(cedula):
					if not alumno.fecha_egr:
						existe = True
			if existe:
				cedExist = True
			else:
				form.save()
				userNew = auth.models.User.objects.create_user(cedula,'',cedula)
				userNew.groups.set('1')
				userOld = auth.models.User.objects.get(username=request.user.username)
				userOld.delete()
				registro = True
				return redirect('logout')
		contexto = {'tipo': str(request.user.groups.get()),'usuario': usuario,'form': form,'registro':registro,'cambiar': True,'cedExist': cedExist}
		return render(request,'Orquesta/modificar_perfil.html',contexto)
	else:
		return redirect('index')

@login_required
def alumnos(request):
	global registro
	if str(request.user.groups.get()) == 'admin':
		alumnosActivos = []
		alumnosInactivos = []
		for alumno in Alumno.objects.all():
			if not alumno.fecha_egr:
				alumnosActivos.append(alumno)
			else:
				alumnosInactivos.append(alumno)
		usuario = Admin.objects.get(cedula=request.user.username)
		contexto = {'tipo': str(request.user.groups.get()),'alumnosActivos': alumnosActivos,'alumnosInactivos': alumnosInactivos,'registro': registro,'usuario': usuario}
		if registro:
			registro = False
		return render(request, 'Orquesta/alumnos.html',contexto)
	elif str(request.user.groups.get()) == 'profesor':
		alumnosAll = []
		alumnosInactivos = []
		for alumno in Alumno.objects.all():
			if not alumno.fecha_egr:
				alumnosAll.append(alumno)
			else:
				alumnosInactivos.append(alumno)
		usuario = Profesor.objects.get(cedula=request.user.username)
		alumnosActivos = []
		for alumno in alumnosAll:
			try:
				if str(alumno.instrumento.profesor.id) == str(usuario.id):
					alumnosActivos.append(alumno)
			except:
				pass
		contexto = {'tipo': str(request.user.groups.get()),'alumnosActivos': alumnosActivos,'registro': registro,'usuario': usuario}
		return render(request, 'Orquesta/alumnos.html',contexto)
	else:
		return redirect('index')

@login_required
def agregar_alumno(request):
	global registro
	global cedExist
	if str(request.user.groups.get()) == 'admin':
		cedExist = False
		usuario = Admin.objects.get(cedula=request.user.username)
		if request.method == 'POST':
			form = AlumnoForm(request.POST)
			if form.is_valid():
				existe = False
				cedula = request.POST.get('cedula')
				alumnos = Alumno.objects.all()
				admins = Admin.objects.all()
				for alumno in alumnos:
					if str(cedula) == str(alumno.cedula):
						existe = True
				for admin in admins:
					if str(cedula) == str(admin.cedula):
						existe = True
				if existe:
					cedExist = True
				else:
					profesores = Profesor.objects.all()
					for profesor in profesores:
						if str(cedula) == str(profesor.cedula):
							existe = True
					if not existe:
						user = auth.models.User.objects.create_user(cedula,'',cedula)
						user.groups.set('3')
					sObject = slice(4)
					fecha = request.POST.get('fecha_nac')
					fecha = int(fecha[sObject])
					hoy = timezone.now()
					if request.POST.get('representante') == '' and fecha + 18 > hoy.year:
						newRep = Representante.objects.create(
							cedula = request.POST.get('cedula_rep'),
							nombre = request.POST.get('nombre_rep'),
							apellido = request.POST.get('apellido_rep'),
							telefono = request.POST.get('telefono_rep'),
							direccion = request.POST.get('direccion_rep'),
							email = request.POST.get('email_rep')
						)
						aluNew = form.save(commit=False)
						aluNew.nombre = aluNew.nombre.capitalize()
						aluNew.apellido = aluNew.apellido.capitalize()
						aluNew.representante = newRep
						aluNew.save()
					else:
						form.save()
					registro = True
					return redirect('alumnos')
		else:
			form = AlumnoForm()

		contexto = {'form': form,'cedExist': cedExist, 'tipo': str(request.user.groups.get()), 'usuario': usuario}
		return render(request, 'Orquesta/nuevo_alumno.html', contexto)
	else:
		return redirect('index')

@login_required
def perfilAlumno(request, alumno_id):
	if str(request.user.groups.get()) == 'admin' or str(request.user.groups.get()) == 'profesor':
		if str(request.user.groups.get()) == 'admin':
			usuario = Admin.objects.get(cedula=request.user.username)
		elif str(request.user.groups.get()) == 'profesor':
			usuario = Profesor.objects.get(cedula=request.user.username)
		alumno = get_object_or_404(Alumno,cedula=alumno_id)
		contexto = {'tipo': str(request.user.groups.get()),'usuario': usuario,'alumno':alumno}
		return render(request,'Orquesta/alumno.html',contexto)
	else:
		return redirect('index')

@login_required
def egresarAlumno(request, alumno_id):
	if str(request.user.groups.get()) == 'admin':
		alumno = get_object_or_404(Alumno,cedula=alumno_id)
		if not alumno.fecha_egr:
			alumno.fecha_egr = timezone.now()
			alumno.save()
			profesores = Profesor.objects.all()
			admins = Admin.objects.all()
			existe = False
			for profesor in profesores:
				if str(alumno.cedula) == str(profesor.cedula):
					existe = True
			for admin in admins:
				if str(alumno.cedula) == str(admin.cedula):
					existe = True
			if not existe:
				user = auth.models.User.objects.get(username=alumno.cedula)
				user.delete()
			return redirect('/alumnos/%s/' %alumno_id)
		else:
			return redirect('/alumnos/%s/' %alumno_id)
	else:
		return redirect('index')

@login_required
def reingresarAlumno(request, alumno_id):
	if str(request.user.groups.get()) == 'admin':
		alumno = get_object_or_404(Alumno,cedula=alumno_id)
		if alumno.fecha_egr:
			profesores = Profesor.objects.all()
			admins = Admin.objects.all()
			existe = False
			for admin in admins:
				if str(alumno.cedula) == str(admin.cedula):
					existe = True
			if not existe:
				for profesor in profesores:
					if str(alumno.cedula) == str(profesor.cedula):
						existe = True
				if not existe:
					user = auth.models.User.objects.create_user(alumno.cedula,'',alumno.cedula)
					user.groups.set('3')
				alumno.fecha_egr = None
				alumno.save()
			return redirect('/alumnos/%s/' %alumno_id)
		else:
			return redirect('/alumnos/%s/' %alumno_id)
	else:
		return redirect('index')

@login_required
def cambiarRepresentante(request, alumno_id):
	global registro
	if str(request.user.groups.get()) == 'admin':
		instance = get_object_or_404(Alumno,cedula=alumno_id)
		form = RepresentanteChangeForm(request.POST or None, instance=instance)
		if form.is_valid():
			if request.POST.get('representante') == '':
				newRep = Representante.objects.create(
					cedula = request.POST.get('cedula_rep'),
					nombre = request.POST.get('nombre_rep'),
					apellido = request.POST.get('apellido_rep'),
					telefono = request.POST.get('telefono_rep'),
					direccion = request.POST.get('direccion_rep'),
					email = request.POST.get('email_rep')
				)
				aluNew = form.save(commit=False)
				aluNew.representante = newRep
				aluNew.save()
			else:
				form.save()
			registro = True
			return redirect('/alumnos/%s/' %alumno_id)
		usuario = Admin.objects.get(cedula=request.user.username)
		contexto = {'tipo': str(request.user.groups.get()),'usuario': usuario,'form': form,'registro':registro}
		return render(request,'Orquesta/cambiar_representante.html',contexto)
	else:
		return redirect('index')

@login_required
def cambiarInstrumento(request, alumno_id):
	global registro
	if str(request.user.groups.get()) == 'admin':
		instance = get_object_or_404(Alumno,cedula=alumno_id)
		form = InstrumentoChangeForm(request.POST or None, instance=instance)
		if instance.fecha_egr:
			if form.is_valid():
				form.save()
				registro = True
				return redirect('/alumnos/%s/' %alumno_id)
		else:
			return redirect('/alumnos/%s/' %alumno_id)
		usuario = Admin.objects.get(cedula=request.user.username)
		contexto = {'tipo': str(request.user.groups.get()),'usuario': usuario,'form': form,'registro':registro}
		return render(request,'Orquesta/cambiar_instrumento.html',contexto)
	else:
		return redirect('index')

@login_required
def expediente(request, alumno_id):
	if str(request.user.groups.get()) == 'admin':
		template = get_template("Reportes/expediente.html")
		actAll = []
		num = 1
		usuario = get_object_or_404(Alumno,cedula=alumno_id)
		for actividad in Actividad.objects.all():
			for alumno in actividad.participantes.all():
				if alumno.id == usuario.id:
					poss = []
					poss.append(num)
					poss.append(actividad)
					actAll.append(poss)
					num += 1
		context = Context({'pagesize':'letter','actividades': actAll,'fecha': timezone.now(),'alumno': usuario})
		html = template.render(context)
		result = StringIO.StringIO()
		pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), dest=result,link_callback=link_callback)
		if not pdf.err:
			return HttpResponse(result.getvalue(), content_type='application/pdf')
		else: return HttpResponse('Errors')
		return ''.join(full_path)
	else:
		return redirect('index')

@login_required
def ascender(request, alumno_id):
	global registro
	alumno = get_object_or_404(Alumno,cedula=alumno_id)
	if str(request.user.groups.get()) == 'admin':
		try:
			if alumno.instrumento.profesor:
				return redirect('index')
		except:
			profesores = Profesor.objects.all()
			admins = Admin.objects.all()
			existe = False
			for admin in admins:
				if str(alumno.cedula) == str(admin.cedula):
					existe = True
			for profesor in profesores:
				if str(alumno.cedula) == str(profesor.cedula):
					existe = True
			if not existe:
				Profesor.objects.create(
						cedula=alumno.cedula,
						nombre=alumno.nombre,
						apellido=alumno.apellido,
						telefono=alumno.telefono,
						direccion=alumno.direccion,
						email=alumno.email,
						instrumento=alumno.instrumento,
						sexo=alumno.sexo,
						foto=alumno.foto,
					)
				if not alumno.fecha_egr:
					user = auth.models.User.objects.get(username=alumno.cedula)
					user.groups.set('2')
				else:
					user = auth.models.User.objects.create_user(alumno.cedula,'',alumno.cedula)
					user.groups.set('2')

			return redirect('/alumnos/%s/' %alumno_id)
	else:
		return redirect('index')

@login_required
def representantes(request):
	global registro
	if str(request.user.groups.get()) == 'admin':
		representantes = Representante.objects.all()
		usuario = Admin.objects.get(cedula=request.user.username)
		contexto = {'tipo': str(request.user.groups.get()),'representantes': representantes,'registro': registro,'usuario': usuario}
		if registro:
			registro = False
		return render(request, 'Orquesta/representantes.html',contexto)
	else:
		return redirect('index')

@login_required
def agregar_representante(request):
	global registro
	global cedExist
	if str(request.user.groups.get()) == 'admin':
		usuario = Admin.objects.get(cedula=request.user.username)
		if request.method == 'POST':
			form = RepresentanteForm(request.POST)
			if form.is_valid():
				existe = False
				cedula = request.POST.get('cedula')
				representantes = Representante.objects.all()
				for representante in representantes:
					if str(cedula) == str(representante.cedula):
						existe = True
				if existe:
					cedExist = True
				else:
					form.save()
					registro = True
					return redirect('representantes')
		else:
			form = RepresentanteForm()

		contexto = {'form': form,'cedExist': cedExist,'tipo': str(request.user.groups.get()), 'usuario': usuario}
		return render(request, 'Orquesta/nuevo_representante.html',contexto)
	else:
		return redirect('index')

@login_required
def perfilRepresentante(request, representante_id):
	global registro
	if str(request.user.groups.get()) == 'admin':
		representante = get_object_or_404(Representante,cedula=representante_id)
		usuario = Admin.objects.get(cedula=request.user.username)
		contexto = {'tipo': str(request.user.groups.get()),'usuario': usuario,'representante':representante,'registro':registro}
		if registro:
			registro = False
		return render(request,'Orquesta/representante.html',contexto)
	else:
		return redirect('index')

@login_required
def modificarPerfilRepresentante(request, representante_id):
	global registro
	if str(request.user.groups.get()) == 'admin':
		instance = get_object_or_404(Representante,cedula=representante_id)
		print(instance)
		form = RepresentanteForm(request.POST or None, instance=instance)
		if form.is_valid():
			form.save()
			registro = True
			return redirect('/representantes/%s' %representante_id)
		usuario = Admin.objects.get(cedula=request.user.username)
		contexto = {'tipo': str(request.user.groups.get()),'usuario': usuario,'form': form,'registro': registro}
		return render(request,'Orquesta/modificar_perfil.html',contexto)
	else:
		return redirect('index')

@login_required
def profesores(request):
	global registro
	if str(request.user.groups.get()) == 'admin':
		profesores = Profesor.objects.all()
		usuario = Admin.objects.get(cedula=request.user.username)
		contexto = {'tipo': str(request.user.groups.get()),'profesores': profesores,'registro': registro,'usuario': usuario}
		if registro:
			registro = False
		return render(request, 'Orquesta/profesores.html',contexto)
	else:
		return redirect('index')

@login_required
def agregar_profesor(request):
	global registro
	global cedExist
	if str(request.user.groups.get()) == 'admin':
		profesores = Profesor.objects.all()
		insVal = []
		for profesor in profesores:
			insVal.append(profesor.instrumento.id)
		usuario = Admin.objects.get(cedula=request.user.username)
		cedExist = False
		if request.method == 'POST':
			form = ProfesorForm(request.POST)
			if form.is_valid():
				existe = False
				cedula = request.POST.get('cedula')
				admins = Admin.objects.all()
				alumnos = Alumno.objects.all()
				for profesor in profesores:
					if str(profesor.cedula) == str(cedula):
						existe = True
				for admin in admins:
					if str(admin.cedula) == str(cedula):
						existe = True
				for alumno in alumnos:
					if str(alumno.cedula) == str(cedula):
						existe = True
				if existe:
					cedExist = True
				else:
					user = auth.models.User.objects.create_user(cedula,'',cedula)
					user.groups.set('2')
					form.save()
					registro = True
					return redirect('profesores')
		else:
			form = ProfesorForm()

		contexto = {'form': form, 'cedExist': cedExist, 'tipo': str(request.user.groups.get()), 'usuario': usuario, 'insVal': insVal}
		return render(request, 'Orquesta/nuevo_profesor.html', contexto)
	else:
		return redirect('index')

@login_required
def perfilProfesor(request, profesor_id):
	if str(request.user.groups.get()) == 'admin':
		profesor = get_object_or_404(Profesor,cedula=profesor_id)
		usuario = Admin.objects.get(cedula=request.user.username)
		contexto = {'tipo': str(request.user.groups.get()),'usuario': usuario,'profesor':profesor}
		return render(request,'Orquesta/profesor.html',contexto)
	else:
		return redirect('index')

@login_required
def retirarProfesor(request, profesor_id):
	if str(request.user.groups.get()) == 'admin':
		profesor = get_object_or_404(Profesor,cedula=profesor_id)
		user = auth.models.User.objects.get(username=profesor.cedula)
		try:
			alumno = Alumno.objects.get(cedula=profesor.cedula)
			if alumno.fecha_egr:
				user.delete()
			else:
				user.groups.set('3')
			profesor.delete()
			return redirect('profesores')
		except:
			user.delete()
			profesor.delete()
			return redirect('profesores')
	else:
		return redirect('index')

@login_required
def instrumentos(request):
	global registro
	if str(request.user.groups.get()) == 'admin':
		ins = Instrumento.objects.all()
		instrumentos = []
		for instrumento in ins:
			pos = []
			alumnos = Alumno.objects.filter(instrumento_id=instrumento.id)
			cantidad = 0
			for alumno in alumnos:
				if not alumno.fecha_egr:
					cantidad += 1
			pos.append(instrumento)
			pos.append(cantidad)
			instrumentos.append(pos)
		usuario = Admin.objects.get(cedula=request.user.username)
		contexto = {'tipo': str(request.user.groups.get()),'instrumentos': instrumentos,'registro': registro,'usuario': usuario}
		if registro:
			registro = False
		return render(request, 'Orquesta/instrumentos.html',contexto)
	else:
		return redirect('index')

@login_required
def agregar_instrumento(request):
	global registro
	if str(request.user.groups.get()) == 'admin':
		if request.method == 'POST':
			form = InstrumentoForm(request.POST)
			if form.is_valid():
				form.save()
				registro = True
			return redirect('instrumentos')
		else:
			form = InstrumentoForm()
		usuario = Admin.objects.get(cedula=request.user.username)
		contexto = {'form': form,'tipo': str(request.user.groups.get()), 'usuario': usuario}
		return render(request, 'Orquesta/nuevo_instrumento.html', contexto)
	else:
		return redirect('index')

@login_required
def instrumentoList(request, instrumento_id):
	if str(request.user.groups.get()) == 'admin':
		instrumento = get_object_or_404(Instrumento,id=instrumento_id)
		alumnos = []
		for alumno in Alumno.objects.filter(instrumento_id=instrumento_id):
			if not alumno.fecha_egr:
				alumnos.append(alumno)
		usuario = Admin.objects.get(cedula=request.user.username)
		contexto = {'tipo': str(request.user.groups.get()),'usuario': usuario,'instrumento':instrumento,'alumnos':alumnos}
		return render(request,'Orquesta/instrumento.html',contexto)
	else:
		return redirect('index')

@login_required
def actividades(request):
	global registro
	if str(request.user.groups.get()) == 'admin':
		actividades = Actividad.objects.all()
		usuario = Admin.objects.get(cedula=request.user.username)
		contexto = {'tipo': str(request.user.groups.get()),'actividades': actividades,'registro': registro,'usuario': usuario}
		if registro:
			registro = False
		return render(request, 'Orquesta/actividades.html',contexto)
	else:
		return redirect('index')

@login_required
def agregar_actividad(request):
	global registro
	if str(request.user.groups.get()) == 'admin':
		if request.method == 'POST':
			form = ActividadForm(request.POST)
			if form.is_valid():
				form.save()
				registro = True
			return redirect('actividades')
		else:
			form = ActividadForm()
		alumnos = []
		alumnosInactivos = []
		for alumno in Alumno.objects.all():
			if not alumno.fecha_egr:
				alumnos.append(alumno)
			else:
				alumnosInactivos.append(alumno)
		usuario = Admin.objects.get(cedula=request.user.username)
		contexto = {
			'form': form,
			'tipo': str(request.user.groups.get()),
			'usuario': usuario,
			'encargados': Profesor.objects.all(),
			'instrumentos': Instrumento.objects.all(),
			'alumnos': alumnos,
			'alumnosInactivos': alumnosInactivos
		}
		return render(request, 'Orquesta/nueva_actividad.html',contexto)
	else:
		return redirect('index')

@login_required
def detallesActividad(request, actividad_id):
	if str(request.user.groups.get()) == 'admin':
		actividad = get_object_or_404(Actividad,id=actividad_id)
		usuario = Admin.objects.get(cedula=request.user.username)
		contexto = {'tipo': str(request.user.groups.get()),'usuario': usuario,'actividad':actividad}
		return render(request,'Orquesta/actividad.html',contexto)
	else:
		return redirect('index')

@login_required
def modificarActividad(request, actividad_id):
	if str(request.user.groups.get()) == 'admin':
		usuario = Admin.objects.get(cedula=request.user.username)
		instance = get_object_or_404(Actividad,id=actividad_id)
		form = ActividadChangeForm(request.POST or None, instance=instance)
		if form.is_valid():
			form.save()
			registro = True
			return redirect('/actividades/%s/' %(actividad_id))
		alumnos = []
		alumnosInactivos = []
		for alumno in Alumno.objects.all():
			if not alumno.fecha_egr:
				alumnos.append(alumno)
			else:
				alumnosInactivos.append(alumno)
		contexto = {
			'form': form,
			'tipo': str(request.user.groups.get()),
			'usuario': usuario,
			'encargados': Profesor.objects.all(),
			'instrumentos': Instrumento.objects.all(),
			'alumnos': alumnos,
			'alumnosInactivos': alumnosInactivos
		}
		return render(request,'Orquesta/modificar_actividad.html',contexto)
	else:
		return redirect('index')

@login_required
def solicitudes(request):
	if str(request.user.groups.get()) == 'admin' or str(request.user.groups.get()) == 'alumno':
		solExist = False
		if str(request.user.groups.get()) == 'admin':
			usuario = Admin.objects.get(cedula=request.user.username)
			solicitudes = Solicitud.objects.all()
		elif str(request.user.groups.get()) == 'alumno':
			usuario = Alumno.objects.get(cedula=request.user.username)
			solAll = Solicitud.objects.all()
			solicitudes = []
			for solicitud in solAll:
				if str(solicitud.alumno.cedula) == str(usuario.cedula):
					solicitudes.append(solicitud)
			if solicitudes:
				solLast = solicitudes[len(solicitudes) - 1]
				if solLast.fecha_sol.year + 1 == timezone.now().year:
					if str(solLast.fecha_sol.month) == "12" and str(timezone.now().month) == "1":
						if solLast.fecha_sol.day <= timezone.now().day:
							solExist = True
				elif solLast.fecha_sol.year == timezone.now().year:
					if solLast.fecha_sol.month == timezone.now().month:
						solExist = True
					elif solLast.fecha_sol.month + 1 == timezone.now().month:
						if solLast.fecha_sol.day <= timezone.now().day:
							solExist = True
			else:
				solExist = False
		contexto = {'tipo': str(request.user.groups.get()),'solicitudes': solicitudes,'usuario': usuario,'solExist': solExist}
		return render(request,'Orquesta/solicitudes.html',contexto)
	else:
		return redirect('index')

@login_required
def evaluaciones(request):
	global registro
	if str(request.user.groups.get()) == 'profesor':
		usuario = Profesor.objects.get(cedula=request.user.username)
		evaAll = Evaluacion.objects.all()
		evaluaciones = []
		for evaluacion in evaAll:
			if evaluacion.alumno.instrumento.profesor.id == usuario.id:
				evaluaciones.append(evaluacion)
		contexto = {'tipo': str(request.user.groups.get()),'evaluaciones': evaluaciones,'registro': registro,'usuario': usuario}
		if registro:
			registro = False
		return render(request, 'Orquesta/evaluaciones.html',contexto)
	else:
		return redirect('index')

@login_required
def agregar_evaluacion(request):
	global registro
	global cedExist
	if str(request.user.groups.get()) == 'profesor':
		if request.method == 'POST':
			form = EvaluacionForm(request.POST)
			if form.is_valid():
				evaluaciones = Evaluacion.objects.all()
				for evaluacion in evaluaciones:
					if str(evaluacion.alumno.id) == str(request.POST.get('alumno')):
						if evaluacion.status == 'E' or evaluacion.status == 'V':
							cedExist = True
				if cedExist == False:
					form.save()
					registro = True
					return redirect('evaluaciones')
		else:
			form = EvaluacionForm()

		alumnosAll = Alumno.objects.all()
		usuario = Profesor.objects.get(cedula=request.user.username)
		alumnos = []
		for alumno in alumnosAll:
			try:
				if str(alumno.instrumento.profesor.id) == str(usuario.id):
					alumnos.append(alumno)
			except:
				pass
		usuario = Profesor.objects.get(cedula=request.user.username)
		contexto = {'form': form,'tipo': str(request.user.groups.get()),'cedExist': cedExist,'usuario': usuario, 'alumnos': alumnos}
		cedExist = False
		return render(request, 'Orquesta/nueva_evaluacion.html', contexto)
	else:
		return redirect('index')

@login_required
def detallesEvaluacion(request, evaluacion_id):
	if str(request.user.groups.get()) == 'profesor':
		usuario = Profesor.objects.get(cedula=request.user.username)
		evaluacion = get_object_or_404(Evaluacion,id=evaluacion_id)
		if str(evaluacion.alumno.instrumento.profesor.id) != str(usuario.id):
			return redirect('index')
		contexto = {'tipo': str(request.user.groups.get()),'usuario': usuario,'evaluacion':evaluacion}
		return render(request,'Orquesta/evaluacion.html',contexto)
	elif str(request.user.groups.get()) == 'alumno':
		evaluacion = get_object_or_404(Evaluacion,id=evaluacion_id)
		if request.method == 'POST':
			evaluacion.urlvideo = request.POST.get('urlvideo')
			evaluacion.status = 'V'
			evaluacion.save()
			return redirect('/evaluaciones/%s' %(evaluacion_id))
		else:
			usuario = Alumno.objects.get(cedula=request.user.username)
			evaluacion = get_object_or_404(Evaluacion,id=evaluacion_id)
			print(str(evaluacion.alumno.id), str(usuario.id))
			if str(evaluacion.alumno.id) != str(usuario.id):
				return redirect('index')
			contexto = {'tipo': str(request.user.groups.get()),'usuario': usuario,'evaluacion':evaluacion}
			return render(request,'Orquesta/evaluacion.html',contexto)

	else:
		return redirect('index')

@login_required
def verVideo(request,evaluacion_id):
	evaluacion = get_object_or_404(Evaluacion,id=evaluacion_id)
	if evaluacion.status == 'E':
		return redirect('/evaluaciones/%s' %(evaluacion_id))
	if str(request.user.groups.get()) == 'profesor':
		if request.method == 'POST':
			if request.POST.get('isTrue') == 'problem':
				evaluacion.status = 'E'
				evaluacion.urlvideo = ''
				evaluacion.save()
				return redirect('/evaluaciones/%s' %(evaluacion_id))
			else:
				evaluacion.status = 'N'
				evaluacion.nota = request.POST.get('nota')
				evaluacion.fecha_fin = timezone.now()
				evaluacion.save()
				return redirect('/evaluaciones/%s' %(evaluacion_id))
		else:
			usuario = Profesor.objects.get(cedula=request.user.username)
			if str(evaluacion.alumno.instrumento.profesor.id) != str(usuario.id):
				return redirect('index')
			contexto = {'tipo': str(request.user.groups.get()),'usuario': usuario,'evaluacion':evaluacion}
			return render(request,'Orquesta/verVideo.html',contexto)
	elif str(request.user.groups.get()) == 'alumno':
		usuario = Alumno.objects.get(cedula=request.user.username)
		if str(evaluacion.alumno.id) != str(usuario.id):
			return redirect('index')
		contexto = {'tipo': str(request.user.groups.get()),'usuario': usuario,'evaluacion':evaluacion}
		return render(request,'Orquesta/verVideo.html',contexto)

	else:
		return redirect('index')

@login_required
def eliminarEvaluacion(request, evaluacion_id):
	if str(request.user.groups.get()) == 'profesor':
		evaluacion = get_object_or_404(Evaluacion,id=evaluacion_id)
		usuario = Profesor.objects.get(cedula=request.user.username)
		if evaluacion.alumno.instrumento.profesor.id == usuario.id and evaluacion.status == 'E':
			evaluacion.delete()
		return redirect('evaluaciones')
	else:
		return redirect('index')

@login_required
def agregar_solicitud(request):
	if str(request.user.groups.get()) == 'alumno':
		solExist = False
		usuario = Alumno.objects.get(cedula=request.user.username)
		solAll = Solicitud.objects.all()
		solicitudes = []
		for solicitud in solAll:
			if str(solicitud.alumno.cedula) == str(usuario.cedula):
				solicitudes.append(solicitud)
		if solicitudes:
			solLast = solicitudes[len(solicitudes) - 1]
			if solLast.fecha_sol.year + 1 == timezone.now().year:
				if str(solLast.fecha_sol.month) == "12" and str(timezone.now().month) == "1":
					if solLast.fecha_sol.day >= timezone.now().day:
						solExist = True
			elif solLast.fecha_sol.year == timezone.now().year:
				if solLast.fecha_sol.month == timezone.now().month:
					solExist = True
				elif solLast.fecha_sol.month + 1 == timezone.now().month:
					if solLast.fecha_sol.day >= timezone.now().day:
						solExist = True
		else:
			solExist = False
		if solExist:
			return redirect('solicitudes')
		else:
			codigo = ''
			minusculas = 'qwertyuiopasdfghjklzxcvbnm'
			mayusculas = 'QWERTYUIOPASDFGHJKLZXCVBNM'
			for x in range(1,51):
				goku = random.randrange(3)
				if goku == 0:
					codigo += str(random.randrange(10))
				elif goku == 1:
					codigo += minusculas[random.randrange(len(minusculas))]
				else:
					codigo += mayusculas[random.randrange(len(mayusculas))]
			solicitud = Solicitud.objects.create(alumno=Alumno.objects.get(id=usuario.id),fecha_sol=timezone.now(),status="E",codigo=codigo)
			return redirect('solicitudes')
		
	else:
		return redirect('index')

@login_required
def eliminarSolicitud(request, solicitud_id):
	if str(request.user.groups.get()) == 'alumno':
		solicitud = get_object_or_404(Solicitud,id=solicitud_id)
		usuario = Alumno.objects.get(cedula=request.user.username)
		if solicitud.alumno.id == usuario.id and solicitud.status == 'E':
			solicitud.delete()
		return redirect('solicitudes')
	else:
		return redirect('index')

@login_required
def notas(request):
	if str(request.user.groups.get()) == 'alumno':
		usuario = Alumno.objects.get(cedula=request.user.username)
		evaAll = Evaluacion.objects.all()
		evaluaciones = []
		for evaluacion in evaAll:
			if str(evaluacion.alumno.id) == str(usuario.id):
				if evaluacion.status == 'N':
					evaluaciones.append(evaluacion)
		contexto = {'tipo': str(request.user.groups.get()),'usuario': usuario,'evaluaciones':evaluaciones}
		return render(request,'Orquesta/notas.html',contexto)
	else:
		return redirect('index')

@login_required
def solicitud(request,solicitud_codigo):
	solicitud = get_object_or_404(Solicitud,codigo=solicitud_codigo)
	if str(request.user.groups.get()) == 'admin':
		if solicitud.status == u'E':
			solicitud.status = u'A'
			solicitud.save()
		return redirect('solicitudes')
	elif str(request.user.groups.get()) == 'alumno':
		if solicitud.status == u'E':
			return redirect('solicitudes')
		elif solicitud.status == u'A':
			if not solicitud.fecha_ent:
				solicitud.fecha_ent = timezone.now()
				solicitud.save()
			template = get_template("Reportes/expediente.html")
			actAll = []
			num = 1
			usuario = Alumno.objects.get(cedula=request.user.username)
			for actividad in Actividad.objects.all():
				for alumno in actividad.participantes.all():
					if alumno.id == usuario.id:
						if actividad.fecha.year < solicitud.fecha_ent.year:
							poss = []
							poss.append(num)
							poss.append(actividad)
							actAll.append(poss)
							num += 1
						elif actividad.fecha.year == solicitud.fecha_ent.year and actividad.fecha.month < solicitud.fecha_ent.month:
							poss = []
							poss.append(num)
							poss.append(actividad)
							actAll.append(poss)
							num += 1
						elif actividad.fecha.year == solicitud.fecha_ent.year and actividad.fecha.month == solicitud.fecha_ent.month and actividad.fecha.day <= solicitud.fecha_ent.day:
							poss = []
							poss.append(num)
							poss.append(actividad)
							actAll.append(poss)
							num += 1
			context = Context({'pagesize':'letter','actividades': actAll,'fecha': solicitud.fecha_ent,'alumno': usuario})
			html = template.render(context)
			result = StringIO.StringIO()
			pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), dest=result,link_callback=link_callback)
			if not pdf.err:
				return HttpResponse(result.getvalue(), content_type='application/pdf')
			else: return HttpResponse('Errors')
			return ''.join(full_path)
	else:
		return redirect('index')

def link_callback(uri, rel):
    sUrl = settings.STATIC_URL
    sRoot = settings.STATIC_ROOT
    mUrl = settings.MEDIA_URL
    mRoot = settings.MEDIA_ROOT

    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri

    if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
    return path

@login_required
def busqueda(request,solicitud_id):
	if str(request.user.groups.get()) == 'admin':
		isNum = 0
		for c in solicitud_id:
			notNum = True
			for i in range(0,10):
				if c == str(i):
					notNum = False
			if notNum:
				isNum += 1
		if isNum != 0:
			solicitudes = []
			alumnos = list(Alumno.objects.filter(nombre__startswith=solicitud_id.capitalize()).values('id'))
			alumnos2 = list(Alumno.objects.filter(apellido__startswith=solicitud_id.capitalize()).values('id'))
			for alumno in alumnos2:
				alumnos.append(alumno)
		else:
			solicitudes = list(Solicitud.objects.filter(id__startswith=solicitud_id).values())
			alumnos = list(Alumno.objects.filter(cedula__startswith=solicitud_id).values('id'))
		#%
		solAll = list(Solicitud.objects.all().values())
		solAlu = []
		for alumno in alumnos:
			for solicitud in solAll:
				if alumno['id'] == solicitud['alumno_id']:
					if solicitudes:
						for sol in solicitudes:
							print(solicitud['id'],sol['id'])
							if solicitud['id'] != sol['id']:
								solAlu.append(solicitud)
					else:
						solAlu.append(solicitud)
		if solAlu:
			for solicitud in solAlu:
				solicitudes.append(solicitud)
		#%
		for solicitud in solicitudes:
			alumno = Alumno.objects.get(id=solicitud['alumno_id'])
			solicitud['foto'] = alumno.foto.url
			solicitud['alumno'] = "%s %s" %(alumno.nombre,alumno.apellido)

		return http.HttpResponse(json.dumps(solicitudes,default=str), content_type='application/json')
	else:
		return redirect('index')