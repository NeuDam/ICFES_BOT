import os
import telebot, time
from icfes import main
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')

#INICIAR CONEXIÓN
bot = telebot.TeleBot(token=TOKEN)

print('CONEXIÓN ESTABLECIDA')

user_data = {}

#COMANDOS
@bot.message_handler(commands=['start'])
def send_welcome(message):
  bot.send_message(message.chat.id, 'Hola! Consulta tu resultado del ICFES ejecutando /consultar')
  bot.send_animation(message.chat.id, 'https://media.giphy.com/media/GiUAFdVYmVgg8/200.gif')


@bot.message_handler(commands=['consultar'])
def iniciar_consulta(message):

    user_data[message.chat.id] = {'step': 1}

    bot.send_message(message.chat.id, "Por favor, ingresa tu NÚMERO DE REGISTRO")

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get('step') == 1)
def manejar_registro(message):

    user_data[message.chat.id]['registro'] = message.text

    bot.send_message(message.chat.id, "Ahora, por favor, ingresa tu numero de documento")

    user_data[message.chat.id]['step'] = 2

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get('step') == 2)
def manejar_documento(message):

    user_data[message.chat.id]['documento'] = message.text

    bot.send_message(message.chat.id, "Por ultimo el tipo de documento (TI,CC)")


    user_data[message.chat.id]['step'] = 3


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get('step') == 3)
def manejar_td(message):
    
  user_data[message.chat.id]['td'] = message.text

  registro = user_data[message.chat.id]['registro']
  documento = user_data[message.chat.id]['documento']
  td = user_data[message.chat.id]['td']

  response,pdf = main(registro,documento,td)

  if 'bad' in response:
    bot.send_message(message.chat.id, 'NO SE ENCONTRÓ EL RESULTADO :(')
  else:
    if pdf == True:
      bot.send_message(message.chat.id, f'HOLA, {response}')
      time.sleep(0.5)
      bot.send_message(message.chat.id, '¿Crees que lo ganaste o lo perdiste?...')
      time.sleep(1.5)

      with open(f'{response}.pdf', 'rb') as f:
        bot.send_document(message.chat.id, f)

      time.sleep(3)

      bot.send_message(message.chat.id, 'Oye... ¿cuánto sacaste? :3')
    else:
      bot.send_message(message.chat.id, response)


  del user_data[message.chat.id]


if __name__ == '__main__':
  bot.polling(non_stop=True)