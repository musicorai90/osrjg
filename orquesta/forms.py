#-*- coding: utf-8 -*-
from django import forms
from .models import *

class AdminForm(forms.ModelForm):

	class Meta:
		model = Admin

		fields = ['cedula','nombre','apellido','telefono','email','direccion',]

		labels = {
			'cedula': 'Cédula',
			'nombre': 'Nombre',
			'apellido': 'Apellido',
			'telefono': 'Teléfono',
			'direccion': 'Dirección',
			'email': 'Email',
		}

		widgets = {
			'cedula': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Cédula','type': 'number','min': '1000000','max': '99999999','autocomplete': 'off','onkeypress': "len8(event,'id_cedula')",'onpaste': 'event.preventDefault()','ondragover': 'event.preventDefault()'}),
			'nombre': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Nombre','onkeypress': 'onlyLetters(event)','onpaste': 'event.preventDefault()','ondragover': 'event.preventDefault()'}),
			'apellido': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Apellido','onkeypress': 'onlyLetters(event)','onpaste': 'event.preventDefault()','ondragover': 'event.preventDefault()'}),
			'telefono': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Teléfono','onkeypress': "telefonoEvent(event,'id_telefono')",'type': 'number','onpaste': 'event.preventDefault()','ondragover': 'event.preventDefault()'}),
			'direccion': forms.Textarea(attrs={'class': 'form-control','placeholder': 'Dirección'}),
			'email': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Correo','type': 'email','onpaste': 'event.preventDefault()','ondragover': 'event.preventDefault()'}),
		}

class AlumnoForm(forms.ModelForm):

	class Meta:
		model = Alumno

		fields = [
			'cedula',
			'nombre',
			'apellido',
			'telefono',
			'email',
			'direccion',
			'instrumento',
			'representante',
			'fecha_nac',
			'fecha_ing',
			'nota_aud',
			'nivel',
			'sexo',
			'cod_ins',
		]

		labels = {
			'cedula': 'Cedula',
			'nombre': 'Nombre',
			'apellido': 'Apellido',
			'telefono': 'Telefono',
			'direccion': 'Direccion',
			'email': 'Email',
			'instrumento': 'Instrumento',
			'representante': 'Representante',
			'fecha_nac': 'Fecha de nacimiento',
			'fecha_ing': 'Fecha de ingreso',
			'nota_aud': 'Nota audicion',
			'nivel': 'Nivel',
			'sexo': 'Sexo',
			'cod_ins': 'Instrumento asignado',
		}

		widgets = {
			'cedula': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Cédula','type': 'number','min': '10000000','max': '99999999','autocomplete': 'off','onkeypress': "len8(event,'id_cedula')",'onpaste': 'event.preventDefault()','ondragover': 'event.preventDefault()'}),
			'nombre': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Nombre','onkeypress': 'onlyLetters(event)','onpaste': 'event.preventDefault()','ondragover': 'event.preventDefault()'}),
			'apellido': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Apellido','onkeypress': 'onlyLetters(event)','onpaste': 'event.preventDefault()','ondragover': 'event.preventDefault()'}),
			'telefono': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Teléfono','onkeypress': "telefonoEvent(event,'id_telefono')",'type': 'number','onpaste': 'event.preventDefault()','ondragover': 'event.preventDefault()'}),
			'direccion': forms.Textarea(attrs={'class': 'form-control','placeholder': 'Dirección'}),
			'email': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Correo','type': 'email','onkeypress': "correoNS(event)",'onpaste': 'event.preventDefault()','ondragover': 'event.preventDefault()'}),
			'instrumento': forms.Select(attrs={'class': 'form-control'}),
			'representante': forms.Select(attrs={'class': 'form-control'}),
			'fecha_nac': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
			'fecha_ing': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
			'nota_aud': forms.TextInput(attrs={'class': 'form-control','placeholder':'10-20','max': '20','type': 'number','autocomplete': 'off','onkeypress': 'valNota(event)','onpaste': 'event.preventDefault()','ondragover': 'event.preventDefault()'}),
			'nivel': forms.Select(attrs={'class': 'form-control'}),
			'sexo': forms.Select(attrs={'class': 'form-control'}),
			'cod_ins': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Código'}),
		}

class RepresentanteForm(forms.ModelForm):

	class Meta:
		model = Representante

		fields = ['cedula','nombre','apellido','telefono','direccion','email',]

		labels = {
			'cedula': 'Cedula',
			'nombre': 'Nombre',
			'apellido': 'Apellido',
			'telefono': 'Telefono',
			'direccion': 'Direccion',
			'email': 'Email',
		}

		widgets = {
			'cedula': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Cédula','type': 'number','min': '1000000','max': '99999999','autocomplete': 'off','onkeypress': "len8(event,'id_cedula')",'onpaste': 'event.preventDefault()','ondragover': 'event.preventDefault()'}),
			'nombre': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Nombre','onkeypress': 'onlyLetters(event)','onpaste': 'event.preventDefault()','ondragover': 'event.preventDefault()'}),
			'apellido': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Apellido','onkeypress': 'onlyLetters(event)','onpaste': 'event.preventDefault()','ondragover': 'event.preventDefault()'}),
			'telefono': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Teléfono','onkeypress': "telefonoEvent(event,'id_telefono')",'type': 'number','onpaste': 'event.preventDefault()','ondragover': 'event.preventDefault()'}),
			'direccion': forms.Textarea(attrs={'class': 'form-control','placeholder': 'Dirección'}),
			'email': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Correo','type': 'email','onpaste': 'event.preventDefault()','ondragover': 'event.preventDefault()'}),
		}

class RepresentanteChangeForm(forms.ModelForm):

	class Meta:
		model = Alumno

		fields = ['representante',]

		labels = {'representante': 'Representante',}

		widgets = {'representante': forms.Select(attrs={'class': 'form-control'}),}

class InstrumentoChangeForm(forms.ModelForm):

	class Meta:
		model = Alumno

		fields = ['instrumento',]

		labels = {'instrumento': 'Instrumento',}

		widgets = {'instrumento': forms.Select(attrs={'class': 'form-control'}),}

class ProfesorForm(forms.ModelForm):

	class Meta:
		model = Profesor

		fields = ['cedula','nombre','apellido','telefono','email','direccion','sexo','instrumento',]

		labels = {
			'cedula': 'Cédula',
			'nombre': 'Nombre',
			'apellido': 'Apellido',
			'telefono': 'Teléfono',
			'direccion': 'Dirección',
			'email': 'Email',
			'sexo': 'Sexo',
			'instrumento': 'Instrumento'
		}

		widgets = {
			'cedula': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Cédula','type': 'number','min': '1000000','max': '99999999','autocomplete': 'off','onkeypress': "len8(event,'id_cedula')",'onpaste': 'event.preventDefault()','ondragover': 'event.preventDefault()'}),
			'nombre': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Nombre','onkeypress': 'onlyLetters(event)','onpaste': 'event.preventDefault()','ondragover': 'event.preventDefault()'}),
			'apellido': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Apellido','onkeypress': 'onlyLetters(event)','onpaste': 'event.preventDefault()','ondragover': 'event.preventDefault()'}),
			'telefono': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Teléfono','onkeypress': "telefonoEvent(event,'id_telefono')",'type': 'number','onpaste': 'event.preventDefault()','ondragover': 'event.preventDefault()'}),
			'direccion': forms.Textarea(attrs={'class': 'form-control','placeholder': 'Dirección'}),
			'email': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Correo','type': 'email','onpaste': 'event.preventDefault()','ondragover': 'event.preventDefault()'}),
			'sexo': forms.Select(attrs={'class': 'form-control'}),
			'instrumento': forms.Select(attrs={'class': 'form-control'}),
		}

class InstrumentoForm(forms.ModelForm):

	class Meta:
		model = Instrumento

		fields = ['nombre']

		labels = {'nombre': 'Nombre'}

		widgets = {'nombre': forms.TextInput(attrs={'class': 'form-control','placeholder':'Instrumento'})}

class ActividadForm(forms.ModelForm):

	class Meta:
		model = Actividad

		fields = ['descripcion','encargado','lugar','fecha','participantes',]

		labels = {
			'descripcion': 'Descripción',
			'encargado': 'Encargado',
			'lugar': 'Lugar',
			'fecha': 'Fecha',
			'participantes': 'Participantes',
		}

		widgets = {
			'descripcion': forms.Textarea(attrs={'class': 'form-control','placeholder': 'Descripción'}),
			'encargado': forms.Textarea(attrs={'class': 'form-control','style': 'display: none;'}),
			'lugar': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Lugar'}),
			'fecha': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
			'participantes': forms.CheckboxSelectMultiple(),
		}

class EvaluacionForm(forms.ModelForm):

	class Meta:
		model = Evaluacion

		fields = ['alumno','contenido','observaciones']

		labels = {
			'alumno': 'Alumno',
			'contenido': 'Contenido',
			'observaciones': 'Observaciones'
		}

		widgets = {
			'alumno': forms.Select(attrs={'class': 'form-control'}),
			'contenido': forms.Textarea(attrs={'class': 'form-control','placeholder': 'Contenido'}),
			'observaciones': forms.Textarea(attrs={'class': 'form-control','placeholder': 'Observaciones'}),
		}

class ActividadChangeForm(forms.ModelForm):

	class Meta:
		model = Actividad
		fields = ['participantes',]
		labels = {'participantes': 'Participantes',}
		widgets = {'participantes': forms.CheckboxSelectMultiple(),}