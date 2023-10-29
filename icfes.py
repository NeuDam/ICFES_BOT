import json
import base64
import requests


def request(doc, reg, td):
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

  response = request(reg=reg, doc=doc, td=td)

  if response == 'bad':
    return 'NO SE ENCONTRÓ EL RESULTADO'
  else:
    return get_data(response)