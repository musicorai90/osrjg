from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

class Admin(models.Model):
	cedula = models.IntegerField()
	nombre = models.CharField(max_length=50)
	apellido = models.CharField(max_length=50)
	telefono = models.BigIntegerField()
	direccion = models.TextField()
	email = models.CharField(max_length=50)
	foto = models.ImageField(upload_to="fotos",default="fotos/profile.png")

	def __unicode__(self):
		cadena = "{0}"
		return cadena.format(self.nombre)

class Representante(models.Model):
	cedula = models.IntegerField()
	nombre = models.CharField(max_length=50)
	apellido = models.CharField(max_length=50)
	telefono = models.BigIntegerField()
	direccion = models.TextField()
	email = models.CharField(max_length=50)

	def __unicode__(self):
		cadena = "{0}"
		return cadena.format(self.cedula)

class Instrumento(models.Model):
	nombre = models.CharField(max_length=50)

	def __unicode__(self):
		cadena = "{0}"
		return cadena.format(self.nombre)

class Alumno(models.Model):
	cedula = models.IntegerField()
	nombre = models.CharField(max_length=50)
	apellido = models.CharField(max_length=50)
	telefono = models.BigIntegerField()
	direccion = models.TextField()
	email = models.CharField(max_length=50)
	instrumento = models.ForeignKey(Instrumento)
	representante = models.ForeignKey(Representante,blank=True,null=True)
	fecha_nac = models.DateField()
	fecha_ing = models.DateField()
	fecha_egr = models.DateField(blank=True,null=True)
	nota_aud = models.IntegerField()
	cod_ins = models.CharField(blank=True,null=True,max_length=30)

	NIVELES = (('Concertino','Concertino'),('Principal','Principal'),('Asistente','Asistente'),('A','A'),('B','B'),('C','C'),('Practicante','Practicante'))
	SEXOS = (('M','M'),('F','F'))

	nivel = models.CharField(max_length=20,choices=NIVELES)
	sexo = models.CharField(max_length=1,choices=SEXOS)
	foto = models.ImageField(upload_to="fotos",default="fotos/profile.png")

	def __unicode__(self):
		cadena = "{0}, {1}"
		return cadena.format(self.apellido,self.nombre)

class Profesor(models.Model):
	cedula = models.IntegerField()
	nombre = models.CharField(max_length=50)
	apellido = models.CharField(max_length=50)
	telefono = models.BigIntegerField()
	direccion = models.TextField()
	email = models.CharField(max_length=50)

	SEXOS = (('M','M'),('F','F'))

	sexo = models.CharField(max_length=1,choices=SEXOS)
	instrumento = models.OneToOneField(Instrumento)
	foto = models.ImageField(upload_to="fotos",default="fotos/profile.png")

	def __unicode__(self):
		cadena = "{0} => {1}"
		return cadena.format(self.nombre,self.instrumento)

class Actividad(models.Model):
	descripcion = models.TextField()
	encargado = models.TextField()
	lugar = models.CharField(max_length=50)
	fecha = models.DateField()
	participantes = models.ManyToManyField(Alumno)

	def __unicode__(self):
		cadena = "{0} - {1} - {2}"
		return cadena.format(self.descripcion,self.lugar,self.encargado)

class Evaluacion(models.Model):
	alumno = models.ForeignKey(Alumno)
	fecha_ini = models.DateField(auto_now_add=True)
	fecha_fin = models.DateField(null=True,blank=True)
	contenido = models.TextField()
	observaciones = models.TextField(null=True,blank=True)
	nota = models.CharField(max_length=3,null=True,blank=True)
	status = models.CharField(max_length=1,default="E")
	urlvideo = models.TextField()

	def __unicode__(self):
		cadena = "{0} - {1}"
		return cadena.format(self.alumno,self.fecha_ini)

class Solicitud(models.Model):
	alumno = models.ForeignKey(Alumno)
	fecha_sol = models.DateField()
	fecha_ent = models.DateField(null=True,blank=True)
	status = models.CharField(max_length=1)
	codigo = models.CharField(max_length=50)

	def __unicode__(self):
		cadena = "{0} - {1}"
		return cadena.format(self.alumno,self.fecha_sol)