var año = 2019;
var mes = 5;
var dia = 12;

function calendario() {
	document.body.innerHTML = `
		<div class="calendario">
			<div class="calendario-content">
				<div class="calendario-header">
					<button id="calendario-izquierda" onclick="antMes();"><i class="fa fa-angle-left"></i></button>
					<div id="calendario-fecha">
						<span id="calendario-mes">Mes</span>
						<span>-</span>
						<span id="calendario-año">Año</span>
					</div>
					<button id="sigMes" class="sigMesHide" id="calendario-derecha" onclick="sigMes();"><i class="fa fa-angle-right"></i></button>
				</div>
				<div class="calendario-mes">
					<div class="calendario-semana">
						<div class="calendario-subtitle"><span>L</span></div>
						<div class="calendario-subtitle"><span>M</span></div>
						<div class="calendario-subtitle"><span>M</span></div>
						<div class="calendario-subtitle"><span>J</span></div>
						<div class="calendario-subtitle"><span>V</span></div>
						<div class="calendario-subtitle"><span>S</span></div>
						<div class="calendario-subtitle"><span>D</span></div>
					</div><div class="calendario-semana">
						<div class="calendario-dia"><span>-</span></div>
						<div class="calendario-dia"><span>-</span></div>
						<div class="calendario-dia"><span>-</span></div>
						<div class="calendario-dia"><span>-</span></div>
						<div class="calendario-dia"><span>-</span></div>
						<div class="calendario-dia"><span>-</span></div>
						<div class="calendario-dia"><span>-</span></div>
					</div>
					<div class="calendario-semana">
						<div class="calendario-dia"><span>-</span></div>
						<div class="calendario-dia"><span>-</span></div>
						<div class="calendario-dia"><span>-</span></div>
						<div class="calendario-dia"><span>-</span></div>
						<div class="calendario-dia"><span>-</span></div>
						<div class="calendario-dia"><span>-</span></div>
						<div class="calendario-dia"><span>-</span></div>
					</div>
					<div class="calendario-semana">
						<div class="calendario-dia"><span>-</span></div>
						<div class="calendario-dia"><span>-</span></div>
						<div class="calendario-dia"><span>-</span></div>
						<div class="calendario-dia"><span>-</span></div>
						<div class="calendario-dia"><span>-</span></div>
						<div class="calendario-dia"><span>-</span></div>
						<div class="calendario-dia"><span>-</span></div>
					</div>
					<div class="calendario-semana">
						<div class="calendario-dia"><span>-</span></div>
						<div class="calendario-dia"><span>-</span></div>
						<div class="calendario-dia"><span>-</span></div>
						<div class="calendario-dia"><span>-</span></div>
						<div class="calendario-dia"><span>-</span></div>
						<div class="calendario-dia"><span>-</span></div>
						<div class="calendario-dia"><span>-</span></div>
					</div>
					<div class="calendario-semana">
						<div class="calendario-dia"><span>-</span></div>
						<div class="calendario-dia"><span>-</span></div>
						<div class="calendario-dia"><span>-</span></div>
						<div class="calendario-dia"><span>-</span></div>
						<div class="calendario-dia"><span>-</span></div>
						<div class="calendario-dia"><span>-</span></div>
						<div class="calendario-dia"><span>-</span></div>
					</div>
					<div class="calendario-semana">
						<div class="calendario-dia"><span>-</span></div>
						<div class="calendario-dia"><span>-</span></div>
						<div class="calendario-dia"><span>-</span></div>
						<div class="calendario-dia"><span>-</span></div>
						<div class="calendario-dia"><span>-</span></div>
						<div class="calendario-dia"><span>-</span></div>
						<div class="calendario-dia"><span>-</span></div>
					</div>
				</div>
			</div>
		</div>
	`;

	llenarCalen();
}

function llenarCalen() {

	var meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]

	document.getElementById('calendario-mes').textContent = meses[mes - 1];
	document.getElementById('calendario-año').textContent = año;

	var añosDia = [];

	var diaUno = 1;
	for (var i = 1900; i <= 2019; i++) {
		if ((i - 1) % 400 == 0) {
			diaUno += 1;
		} else if ((i - 1) % 100 != 0) {
			if ((i - 1) % 4 == 0) {
				diaUno += 1;
			}
		}

		if (diaUno > 7) {
			diaUno -= 7;
		}

		añosDia.push(diaUno);
		diaUno += 1;
	}

	var mesesDur = [31,28,31,30,31,30,31,31,30,31,30,31];

	var isBis = false;

	if (año % 400 == 0) {
		isBis = true;
	} else if (año % 100 != 0) {
		if (año % 4 == 0) {
			isBis = true;
		}
	}

	if (isBis) { mesesDur[1] = 29 }

	var diaIni = añosDia[año - 1900];
	for (var i = 0; i < mes-1; i++) {
		diaIni += mesesDur[i];
	}

	while (diaIni >= 7) {
		diaIni -= 7;
	}

	if (diaIni == 0) {
		diaIni = 6;
	} else {
		diaIni -= 1
	}

	var diaCon = 1;
	var dias = document.getElementsByClassName('calendario-dia');

	for (var i = 0; i < dias.length; i++) {
		dias[i].style.background = "#eee";
		dias[i].style.cursor = "default";
		dias[i].firstChild.textContent = "-";
	}

	for (var i = diaIni; i < (mesesDur[mes-1]) + (diaIni); i++) {
		dias[i].style.background = "#fff";
		dias[i].style.cursor = "pointer";
		dias[i].firstChild.textContent = diaCon;
		diaCon += 1;
	}
}

function antMes() {
	if (document.getElementById('sigMes').classList.contains('sigMesHide')) {
		document.getElementById('sigMes').classList.remove('sigMesHide');
	}
	if (mes == 1) {
		año -= 1;
		mes = 12;
	} else {
		mes -= 1;
	}
	llenarCalen();
}

function sigMes() {
	if (año == 2019) {
		if (mes < 5) {
			mes += 1;
			llenarCalen();
			if (mes == 5) {
				document.getElementById('sigMes').classList.add('sigMesHide');
			}
		}
	} else if (año < 2019) {
		if (mes == 12) {
			año += 1;
			mes = 1;
		} else {
			mes += 1;
		}
		llenarCalen();
	}
}