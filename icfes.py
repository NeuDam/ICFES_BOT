import json
import base64
import requests


def first_request(doc,reg,td):
  
  data_dx = {
    "tipoDocumento": td.upper(),
    "numeroDocumento": doc,
    "fechaNacimiento": None,
    "identificacionUnica": reg.upper()
  }

  r = requests.post('https://resultadosbackend.icfes.gov.co/api/segurity/autenticacionResultados', json=data_dx).json()

  try:
    fecha_nacimiento = r.get('datosAutenticacion')[0].get('datosParametros').get('fechaNacimiento')
  except:
    return 'bad'

  token = r.get('token')

  r = requests.get(url=f'https://resultadosbackend.icfes.gov.co/api/datos-basicos/datosBasicosRespuesta?examen=SB11&identificacionUnica={reg.upper()}', headers={'Authorization': token}).json()

  periodo = r.get('periodoResultado')
  nombre = r.get('camposDatosBasicos')[0].get('valorDatoBasico')
  colegio = r.get('camposDatosBasicos')[7].get('valorDatoBasico')

  r = requests.get(url=f'https://resultadosbackend.icfes.gov.co/api/resultados/datosReporteGeneral?identificacionUnica={reg.upper()}&examen=SB11&periodoAnioExamen={periodo}',  headers={'Authorization': token}).json()


  resultado = r.get('resultadosGenerales').get('puntajeGlobal')
  perc = r.get('resultadosGenerales').get('percentilNacional')

  final_message = f'''
Oye, {nombre} obtuviste <{resultado}>. Nacido el {fecha_nacimiento}.
Colegio: {colegio}.
Tu puntaje está por encima del {perc}% a nivel nacional.
  '''

  return final_message

def second_request(doc, reg, td):
  url = 'https://resultadosbackend.icfes.gov.co/api/seguritypro/resultadosGeneral/unificacionResultados/consultar'

  headers = {
    'Content-Type': 'application/json',
    'Authorization': 'null',
  }

  data = {
    "tipoDocumento": td.upper(),
    "numeroDocumento": doc,
    "fechaNacimiento": None,
    "numeroRegistro": reg.upper()
  }

  response = requests.post(url, headers=headers, json=data).text

  try:
    response = json.loads(response)[0]
    return response
  except IndexError:
    return 'bad'

def get_data(response):
    
  json_data = {
    'NOMBRE': response.get('nombreComplento'),
    'FECHA DE EXAMEN': response.get('fechaPresentacion')
  }

  pdf_data = response.get('pdf')[0].get('PDF64')

  base64_data = pdf_data.split(",", 1)[1]

  pdf_data = base64.b64decode(base64_data)

  with open(f"{json_data.get('NOMBRE')}.pdf", "wb") as pdf_file:
    pdf_file.write(pdf_data)

  return json_data.get('NOMBRE')


def main(reg,doc,td):

  response = first_request(reg=reg, doc=doc, td=td)

  if response != 'bad':
    return response, False

  response = second_request(reg=reg, doc=doc, td=td)

  if response == 'bad':
    return 'bad', False
  else:
    return get_data(response), True