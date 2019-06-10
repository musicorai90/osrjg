window.onload = load;

function load() {
	var container = document.getElementById("container");
	if (container) {
		container.classList.add('cerrar');
		return setTimeout(function() {
			container.style.display = "none";
		}, 500);
	}
}

function expandir(obj) {
	elem = document.getElementById(obj);
	i = document.getElementById(obj+'_i')
	lista = elem.classList.valueOf();
	if (lista[1] == 'active') {
		elem.style.animation = "cerrar 0.5s ease-out";
		elem.classList.remove('active');
		elem.style.marginBottom = "-2px";
		elem.style.opacity = "0";
		i.classList.remove('active');
	} else {
		elem.style.animation = "abrir 1s ease-in";
		elem.classList.add('active');
		elem.style.marginBottom = "0px";
		elem.style.opacity = "1";
		i.classList.add('active');
	}
}

function menuAction() {
	var left = document.getElementById('orq-bar');
	var right = document.getElementById('orq-general');
	var lista = left.classList;
	if (lista[lista.length - 1] == "active") {
		left.classList.remove("active");
		right.classList.remove("active");
	} else {
		left.classList.add("active");
		right.classList.add("active");
	}
}

function redireccionar(url) {
	window.location.replace(url);
}

function quitarInputs() {
	var elementos = document.getElementsByTagName('input');
	for (var i = elementos.length - 1; i >= 0; i--) {
		if (elementos[i].type == "text") {
			var padre = elementos[i].parentElement;
			var texto = padre.firstElementChild.textContent;
			var ph = texto.slice(0,-1);
			padre.lastElementChild.placeholder = ph;
		}
	}
}

function eliminar(nombre,lista) {
	var labels = document.getElementsByTagName('label');
	for (var i = labels.length - 1; i >= 0; i--) {
		if (labels[i].htmlFor == nombre) {
			lista.push(labels[i]);
		}
	}

	lista[lista.length - 1].parentElement.style.display = "none";
}

function eliminarP_vacias() {
	var elemP = document.getElementsByTagName('p');
	for (var i = elemP.length - 1; i >= 0; i--) {
		if ((elemP[i].childElementCount == 0)&&(elemP[i].childElementCount == "")) {
			elemP[i].style.display = "none";
		}
	}
}

function selects(id_campo_0,nuevoTextContent,nuevo_div,select,nuevo_ul,lista_nueva,id_campo,id_label,id_label_0) {

	var formulario = document.getElementById("orq-form");

	document.getElementById(id_campo_0).parentElement.textContent = nuevoTextContent;

	formulario.insertBefore(nuevo_div,select);
	nuevo_div.classList.add("select");
	nuevo_div.appendChild(nuevo_ul);
	for (var i = select.children.length - 1; i >= 0; i--) {
		lista_nueva.push(select.children[i].firstElementChild)
	}

	function mostrar_li() {
		var hay = 0;
		for (var i = lista_nueva.length - 1; i >= 0; i--) {
			if (lista_nueva[i].classList.contains("active")) {
				hay += 1;
			}
		}
		if (hay == 1) {
			for (var i = lista_nueva.length - 1; i >= 0; i--) {
				if (lista_nueva[i].classList.contains("active") == false) {
					lista_nueva[i].classList.add("active");
				}
			}
			document.getElementById(id_campo).classList.add('active');
			hay = 0;
		} else {
			for (var i = lista_nueva.length - 1; i >= 0; i--) {
				lista_nueva[i].classList.remove("active");
			}
			var label_text = this.textContent;
			lista_nueva[lista_nueva.length - 1].classList.add("active");
			lista_nueva[lista_nueva.length - 1].textContent = label_text;
			if (this.firstElementChild != null) {
				this.firstElementChild.click();
			}
			document.getElementById(id_campo).classList.remove('active');
			hay = 0;
		}
	}

	var numerito = 0;
	for (var i = lista_nueva.length - 1; i >= 0; i--) {
		nuevo_ul.appendChild(lista_nueva[i]);
		lista_nueva[i].id = id_label + numerito;
		if (i == lista_nueva.length - 1) {
			lista_nueva[i].style.fontWeight = "500";
		} else {
			lista_nueva[i].style.fontWeight = "300";
		}
		lista_nueva[i].addEventListener('click',mostrar_li);
		numerito += 1; 
	}
	document.getElementById(id_label_0).classList.add("active");
	select.style.display = "none";
	select.id = "";
	nuevo_ul.id = id_campo;
}

function estilosDeIputsDates() {
	var inputDates = document.getElementsByTagName('select');
	for (var i = inputDates.length - 1; i >= 0; i--) {
		if (inputDates[i].parentElement.classList.contains("inputDate") == false) {
			inputDates[i].parentElement.classList.add("inputDate");
		}
	}
}

function estilosButton() {
	var formulario = document.getElementById("orq-form");
	var nuevo_div_button = document.createElement("DIV");
	var ultimoElem = formulario.children[formulario.children.length - 1];

	formulario.insertBefore(nuevo_div_button,ultimoElem);
	nuevo_div_button.classList.add("button-content");
	nuevo_div_button.appendChild(ultimoElem);
	ultimoElem.classList.add("orq-btn");
}

function lista_años(id_fecha,inicio) {
	var años = document.getElementById(id_fecha);
	for (var i = años.children.length - 1; i >= 0; i--) {
		años.children[i].style.display = "none";
	}
	for (var i = inicio; i >= inicio - 30; i--) {
		var año = document.createElement("OPTION");
		años.appendChild(año);
		año.value = i;
		año.textContent = i;
		if (i == inicio) {
			año.defaultSelected = true;
		}
	}
}

function labelsDates() {
	var inputDates = document.getElementsByClassName('inputDate');
	for (var i = inputDates.length - 1; i >= 0; i--) {
		inputDates[i].firstElementChild.style.display = "block";
		inputDates[i].firstElementChild.style.width = "100%";
		inputDates[i].firstElementChild.style.fontWeight = "500";
	}
}

function llenar() {
	var encargados = '';
	if (document.getElementById("otros_encargados").value != '') {
		var enc_text = document.getElementById("otros_encargados").value + ", ";
		encargados += enc_text;
	}
	var ul_e = document.getElementById("encargados");
	for (var i = ul_e.children.length - 1; i >= 0; i--) {
		var encar = ul_e.children[i].firstElementChild.firstElementChild;
		if (encar.checked) {
			var enc_text2 = encar.value + ", ";
			encargados += enc_text2;
		}
	}
	var encargadosText = '';
	for (var i = 0; i < encargados.length; i++) {
		if (i != encargados.length - 2) {
			encargadosText += encargados[i];
		}
	}
	document.getElementById("id_encargado").value = encargadosText;
	document.getElementById("btn-submit").click();
}

function actividades() {
	document.getElementById("id_participantes").classList.add("participantes");
	var form_p = document.getElementById('orq-form');
	var label_p = document.createElement("LABEL");
	var label_e = document.createElement('LABEL');
	label_p.textContent = "Participantes:";
	label_e.textContent = "Encargados:";
	var ul_p = document.getElementById("id_participantes");
	form_p.insertBefore(label_p,ul_p);
	form_p.insertBefore(label_e,ul_p);
	label_p.classList.add('label_p');
	label_e.classList.add('label_p');
	label_e.style.paddingLeft = "1rem";
	form_p.children[form_p.length - 5].style.display = "none";
}

var openFile = function(event) {
	var input = event.target;

	var reader = new FileReader();
	reader.onload = function() {
		var dataURL = reader.result;
		var outpout = document.getElementById("orq-img-nueva");
		outpout.src = dataURL;
	};
	reader.readAsDataURL(input.files[0]);
	var elems = document.getElementById('orq-form').children;
	for (var i = elems.length - 1; i >= 0; i--) {
		if (elems[i].tagName == "DIV") {
			elems[i].style.display = "block";
			elems[i].style.width = "100%";
			if (elems[i].classList.contains('orq-img-nueva-button')) {
				elems[i].style.display = "flex";
			}
		} else {
			if (elems[i].tagName == "BUTTON") {
				elems[i].style.display = "none";
			}
		}
	}
}

function onlyLetters(e) {
	var val = false;
	var letters = "abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
	for (var i = 0; i < letters.length; i++) {
		if (e.key == letters[i]) {
			val = true;
		}
	}
	if ((!val)&&(e.key != ' ')) {
		e.preventDefault();
	}
}

function len8(e,id) {
	if (document.getElementById(id).value.length + 1 == 9 || e.key == 'e' || e.key == '+' || e.key == '-') {
		e.preventDefault();
	}
}

/*function telefonos() {
	document.getElementById('id_telefono').style.display = "none";
	var nuevo_div_tel = document.createElement("DIV");
	document.getElementById('id_telefono').parentElement.appendChild(nuevo_div_tel);
	nuevo_div_tel.classList.add('form-telefonos');
	var nuevo_select = document.createElement("SELECT");
	var codigos = ['Codigo','0412','0414','0416','0424','0426','0257'];
	var options = []
	for (var i = codigos.length - 1; i >= 0; i--) {
		var option = document.createElement("OPTION");
		option.value = codigos[i];
		option.textContent = codigos[i];
		options.push(option);
	}
	for (var i = options.length - 1; i >= 0; i--) {
		nuevo_select.appendChild(options[i]);
	}
	nuevo_select.id = "codigos";
	nuevo_div_tel.appendChild(nuevo_select);
	var nuevo_input = document.createElement("INPUT");
	nuevo_div_tel.appendChild(nuevo_input);
	nuevo_input.type = "number";
	nuevo_input.placeholder = "Telefono";
	nuevo_input.autocomplete = "off";
	nuevo_input.id = "telefono7";
	nuevo_input.required = true;

	document.getElementById('codigos').required = true;
	document.getElementById('codigos').firstElementChild.value = "";
	document.getElementById('codigos').firstElementChild.disabled = true;

	nuevo_select.classList.add('form-control');
	nuevo_input.classList.add('form-control');
}*/

function telefonoEvent(e,elem) {
	var status = false;
	var numeros = "1234567890";
	var telefono = document.getElementById(elem);
	if (telefono.value.length + 1 == 12) {
		e.preventDefault();
	} else {
		for (var i = numeros.length - 1; i >= 0; i--) {
			if (e.key == numeros[i]) {
				status = true;
			}
		}
		if (!status) {
			e.preventDefault();
		} else {
			if ((telefono.value.length == 0)&&(e.key != "0")) {
				e.preventDefault();
			} else if (telefono.value.length == 1) {
				if ((e.key != '2')&&(e.key != '4')) {
					e.preventDefault();
				}
			} else if (telefono.value.length == 2) {
				if (telefono.value[1] == '4') {
					if ((e.key != '1')&&(e.key != '2')) {
						e.preventDefault();
					}
				}
			} else if (telefono.value.length == 3) {
				if (telefono.value[1] == '4') {
					if (telefono.value[2] == '1') {
						if ((e.key != '2')&&(e.key != '4')&&(e.key != '6')) {
							e.preventDefault();
						}
					} else {
						if ((e.key != '4')&&(e.key != '6')) {
							e.preventDefault();
						}
					}
				}
			}
		}
	}
}


function validarSelects(nam) {
	var insInputs = document.getElementsByName(nam);
	var checkExist = false;
	for (var i = insInputs.length - 1; i >= 0; i--) {
		if (insInputs[i].checked) {
			checkExist = true;
		}
	}
	if (!checkExist) {
		alert("Por favor, selecciones un " + nam + ".");
	}
	return false;
}

function valNota(e) {
	if (document.getElementById('id_nota_aud').value.length == 2) {
		e.preventDefault();
	} else {
		var telVal = false;
		for (var i = 0; i < 10; i++) {
			if (e.key == i) {
				telVal = true;
			}
		}
		if (!telVal) {
			e.preventDefault();
		}
	}
}

function valNotaDos(e) {
	if (document.getElementById('nota').value.length == 2) {
		e.preventDefault();
	} else {
		var telVal = false;
		for (var i = 0; i < 10; i++) {
			if (e.key == i) {
				telVal = true;
			}
		}
		if (!telVal) {
			e.preventDefault();
		}
	}
}


function changePass() {
	if (document.getElementById('contrasena2').value != document.getElementById('contrasena').value) {
		document.getElementById('contrasena-error').classList.add('block');
		return setTimeout(function() {
			document.getElementById('contrasena-error').style.opacity = "1";
		}, 500);
	} else {
		document.getElementById('guardar-btn').click();
	}
}

function reEnter(e) {
	if (e.key == "Enter") {
		e.preventDefault();
		document.getElementById('guardar').click();
	}
}

function inputsReEnter() {
	var inputs = document.getElementsByTagName('input');
	for (var i = inputs.length - 1; i >= 0; i--) {
		inputs[i].addEventListener('keypress',reEnter);
	}
}

function modalRepresentante() {
	document.getElementById('modal-representante').style.display = "flex";
	return setTimeout(function() {
		document.getElementById('modal-representante').style.opacity = "1";
		document.getElementById('modal-representante-content').classList.add('active');
	},500);
}

function cerrarModal() {
	document.getElementById('modal-representante').style.opacity = "0";
	document.getElementById('modal-representante-content').classList.remove('active');
	return setTimeout(function() {
		document.getElementById('modal-representante').style.display = "none";
	},600);
}

function telefonoFull(inputTel) {
	var telValue = document.getElementById(inputTel).value;
	if (telValue.length != 11) {
		return 'El teléfono debe contener 11 dígitos';
	} else if ((telValue.slice(0,4) != '0412')&&(telValue.slice(0,4) != '0414')&&(telValue.slice(0,4) != '0416')&&(telValue.slice(0,4) != '0424')&&(telValue.slice(0,4) != '0426')&&(telValue.slice(0,2) != '02')) {
		return 'Ingrese un código válido';
	} else {
		return false;
	}
}

function validarAlumno() {
	var id_cedula = document.getElementById('id_cedula').value;
	var id_nombre = document.getElementById('id_nombre').value;
	var id_apellido = document.getElementById('id_apellido').value;
	var id_telefono = document.getElementById('id_telefono').value;
	var id_direccion = document.getElementById('id_direccion').value;
	var id_email = document.getElementById('id_email').value;
	var id_instrumento = document.getElementById('id_instrumento').value;
	var id_representante = document.getElementById('id_representante');
	var id_fecha_nac = document.getElementById('id_fecha_nac').value;
	var id_fecha_ing = document.getElementById('id_fecha_ing').value;
	var id_nivel = document.getElementById('id_nivel').value;
	var id_sexo = document.getElementById('id_sexo').value;
	var id_nota_aud = document.getElementById('id_nota_aud').value;

	var telefonoVal = telefonoFull("id_telefono");

	var valCorreo = false;
	var conCorreo = 0;
	for (var i = 0; i < id_email.length - 1; i++) {
		if (id_email[i] == '@') {
			valCorreo = true;
			conCorreo += 1;
		}
	}
	if ((id_email[0] == '@')||(id_email[id_email.length - 1] == '@')) {
		valCorreo = false
	} else if (conCorreo == 1) {
		valCorreo = true;
	} else if (conCorreo != 1) {
		valCorreo = false;
	}

	var fechaNac = document.getElementById("id_fecha_nac").value.slice(0,4);
	var fechaIng = document.getElementById("id_fecha_ing").value.split('-');
	var now = new Date();
	
	var representanteVal = false;
	if (Number(fechaNac) + 18 <= now.getFullYear()) {
		representanteVal = true;
	}

	var isVal = true;

	if ((!id_cedula)||(!id_nombre)||(!id_apellido)||(!id_telefono)||(!id_direccion)||(!id_email)||(!id_instrumento)||((!id_representante.value)&&(!id_representante.classList.contains('active'))&&(!representanteVal))||(!id_fecha_nac)||(!id_fecha_ing)||(!id_nivel)||(!id_sexo)||(!id_nota_aud)) {
		isVal = false;
		alert('Por favor, rellene todos los campos');
	} else if (document.getElementById('id_cedula').value < 10000000) {
		isVal = false;
		alert('Hay un problema con su cédula');
	} else if (telefonoVal) {
		isVal = false;
		alert(telefonoVal);
	} else if (!valCorreo) {
		isVal = false;
		alert('Ingrese un correo correcto');
	} else if ((id_nota_aud > 20)||(id_nota_aud < 10)) {
		isVal = false;
		alert('La nota debe ser entre 10 y 20');
	} else if ((fechaNac > now.getFullYear() - 10)||(fechaNac < now.getFullYear() - 30)) {
		isVal = false;
		alert('Está edad no está permitida');
	} else if (fechaIng[0] == now.getFullYear()) {
		if (fechaIng[1] == now.getMonth() + 1) {
			if (fechaIng[2] > now.getDate()) {
				isVal = false;
				alert('Por favor, ingrese una fecha de ingreso válida');
			}
		} else if (fechaIng[1] > now.getMonth() + 1) {
			isVal = false;
			alert('Por favor, ingrese una fecha de ingreso válida');
		}
	} else if (fechaIng[0] > now.getFullYear()) {
		isVal = false;
		alert('Por favor, ingrese una fecha de ingreso válida');
	} else if (fechaIng[0] < now.getFullYear()) {
		if (fechaNac > fechaIng[0] - 10) {
			isVal = false;
			alert('Por favor, ingrese una fecha de ingreso válida');
		}
	}

	if (isVal) {
		document.getElementById('orq-form').submit();
	}
}


function alumnoRep() {
	var cedula_rep = document.getElementById('cedula_rep').value;
	var nombre_rep = document.getElementById('nombre_rep').value;
	var apellido_rep = document.getElementById('apellido_rep').value;
	var telefono_rep = document.getElementById('telefono_rep').value;
	var direccion_rep = document.getElementById('direccion_rep').value;
	var email_rep = document.getElementById('email_rep').value;
	
	// Cédula
	var cedulaExist = false;
	for (var i = 0; i < document.getElementById('id_representante').children.length; i++) {
		if (cedula_rep == document.getElementById('id_representante').children[i].textContent) {
			cedulaExist = true;
		}
	}

	//Teléfono
	var telefonoVal = telefonoFull("telefono_rep");

	//Mail
	var valCorreo = false;
	var conCorreo = 0;
	for (var i = 0; i < email_rep.length - 1; i++) {
		if (email_rep[i] == '@') {
			valCorreo = true;
			conCorreo += 1;
		}
	}
	if ((email_rep[0] == '@')||(email_rep[email_rep.length - 1] == '@')) {
		valCorreo = false
	} else if (conCorreo == 1) {
		valCorreo = true;
	} else if (conCorreo != 1) {
		valCorreo = false;
	}
	
	//Condicionales
	if ((cedula_rep == '')||(nombre_rep == '')||(apellido_rep == '')||(telefono_rep == '')||(direccion_rep == '')||(email_rep == '')) {
		alert('Por favor, rellene todos los campos.');
	} else if (cedula_rep < 1000000) {
		alert('Hay un problema con su cédula');
	} else if (cedulaExist) {
		alert('Esta cedula ya está registrada');
	} else if (!valCorreo) {
		alert('Ingrese un correo valido');
	} else if (telefonoVal){
		alert(telefonoVal);
	} else {
		document.getElementById('id_representante').firstElementChild.textContent = cedula_rep;
		document.getElementById('id_representante').required = false;
		//document.getElementById('id_representante').firstElementChild.value = "-1";
		document.getElementById('addRepresentante').innerHTML = "<i class='fa fa-check'></i>";
		document.getElementById('id_representante').classList.add('active');
		cerrarModal();
	}
}

function enterAluRep() {
	for (var i = 0; i < document.getElementById('modal-representante').getElementsByTagName('input').length; i++) {
		document.getElementById('modal-representante').getElementsByTagName('input')[i].removeEventListener('keypress',reEnter)
		document.getElementById('modal-representante').getElementsByTagName('input')[i].addEventListener('keypress',function(event) {
			if (event.key == 'Enter') {
				document.getElementById('guardar-representante').click();
			}
		})
	}
}

function correoNS(event) {
	if (event.key == ' ') {
		event.preventDefault();
	}
}

function inputDisabled(e) {
	e.preventDefault();
}

function validarAdminRepPro() {
	var telefonoval = telefonoFull('id_telefono');
	if (telefonoval) {
		alert(telefonoval);
	} else {
		document.getElementById('guardar-btn').click();
	}
}

function validateCheck(list) {
	var list2 = document.getElementById(list).getElementsByTagName('input');
	for (var i = 0; i < list2.length; i++) {
		if (list2[i].checked) {
			return true;
		}
	}
	return false;
}

function validarAct() {
	var id_fecha = document.getElementById('id_fecha').value.split('-');
	var now = new Date();

	var parVal = validateCheck('id_participantes');
	var encVal = validateCheck('id_encargados');
	var encOthersVal = document.getElementById('otros_encargados').value;

	var forVal = true;	

	if ((!parVal)||((!encVal)&&(!encOthersVal))) {
		forVal = false;
		alert('Por favor, llene todos los campos');
	} else if (id_fecha[0] > now.getFullYear()) {
		forVal = false;
		alert('Por favor, ingrese una fecha de ingreso válida');
	} else if (id_fecha[0] == now.getFullYear()) {
		if (id_fecha[1] > now.getMonth() + 1) {
			forVal = false;
			alert('Por favor, ingrese una fecha de ingreso válida');
		} else if (id_fecha[1] == now.getMonth() + 1) {
			if (id_fecha[2] > now.getDate()) {
				forVal = false;
				alert('Por favor, ingrese una fecha de ingreso válida');
			}
		} else if (id_fecha[1] < now.getMonth() + 1) {
			if (now.getMonth() + 1 > 4) {
				if (id_fecha[1] < now.getMonth() - 2) {
					forVal = false;
					alert('Por favor, ingrese una fecha de ingreso válida');
				}
			}
		}
	} else {
		if (Number(id_fecha[0]) + 1 != now.getFullYear()) {
			forVal = false;
			alert('Por favor, ingrese una fecha de ingreso válida');
		} else {
			if (now.getMonth() > 2) {
				forVal = false;
				alert('Por favor, ingrese una fecha de ingreso válida');
			} else {
				if ((now.getMonth() + 13) - Number(id_fecha[1]) > 3) {
					forVal = false;
					alert('Por favor, ingrese una fecha de ingreso válida');
				}
			}
		}
	}

	if (forVal) {
		var encargadosInput = document.getElementById('id_encargado');
		var encargados = document.getElementById('id_encargados').getElementsByTagName('input');
		var encargadosOthers = document.getElementById('otros_encargados');
		
		for (var i = 0; i < encargados.length; i++) {
			if (encargados[i].checked) {
				encargadosInput.value += encargados[i].value + ", ";
			}
		}

		if (encargadosOthers.value) {
			encargadosInput.value += encargadosOthers.value;
		} else {
			encargadosInput.value = encargadosInput.value.slice(0,encargadosInput.value.length - 2);
		}
		document.getElementById('guardar-btn').click();
	}
}

function readOnlySelect(idSelect,valueSelect) {
	var selectX = document.getElementById(idSelect);
	selectX.style.background = "#ddd";
	for (var i = 0; i < selectX.length; i++) {
		selectX.options[i].style.display = "none";
		if (selectX.options[i].value == valueSelect) {
			selectX.selectedIndex = i;
		} else {
			selectX.options[i].disabled = true;
		}
	}
}

function addItem() {
	var divNew = document.createElement('DIV');
	var inputNew = document.createElement('INPUT');
	document.getElementById('items').appendChild(divNew);
	divNew.appendChild(inputNew);
	divNew.classList.add('orq-col')
	inputNew.type = "text";
	inputNew.classList.add('form-control');
	inputNew.placeholder = "Item " + (document.getElementById('items').getElementsByTagName('input').length);
	inputNew.addEventListener('keypress',reEnter);
}