import base64
import requests


def first_request(doc,reg,td):

  data_dx = {
    "tipoDocumento": td.upper(),
    "numeroDocumento": doc,
    "fechaNacimiento": None,
    "identificacionUnica": reg.upper()
  }

  try:
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
  except:
    return 'bad'

  final_message = f'''
Oye, {nombre} obtuviste <{resultado}>. Nacido el {fecha_nacimiento}.
Colegio: {colegio}.
Tu puntaje está por encima del {perc}% a nivel nacional.
  '''

  return final_message

def main(reg,doc,td):

  response = first_request(reg=reg, doc=doc, td=td)

  if response != 'bad':
    return response, False

  else:
    return 'bad', False
