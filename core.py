import logging
import requests
import telebot
import json
import os
from flask import Flask, request
import random
from textwrap import wrap
from translate import Translator

server = Flask(__name__)

TOKEN = "YOUR TELEGRAM TOKEN"
bot = telebot.TeleBot(TOKEN,parse_mode=None)

GROUP_ID = YOUR GROUP ID

def pigImage():


    url = "https://pigs.p.rapidapi.com/random"

    headers = {
        'x-rapidapi-key': "RAPID API KEY",
        'x-rapidapi-host': "pigs.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers)

    resp = response.json()
    return (resp['source'])

def corgiImage():

    url = "https://dog.ceo/api/breed/pembroke/images"
    response = requests.request("GET", url).json()
    
    return (random.choice(response['message']))

def covidBrazil():

    url = "https://covid-19-data.p.rapidapi.com/country"

    querystring = {"name":"brazil"}

    headers = {
        'x-rapidapi-key': "RAPID API KEY",
        'x-rapidapi-host': "covid-19-data.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring).json()

    confirmados = response[0]['confirmed']
    recuperados = response[0]['recovered']
    mortes = response[0]['deaths']
    finalupdate = wrap(response[0]['lastUpdate'], 10)

    linha1 = f"Casos de Covid-19 no Brasil!\n\n"
    linha2 = f"Confirmados: {confirmados}\nRecuperados: {recuperados}\nMortes: {mortes}\n"
    linha3 = f"Ultima Atualização: {finalupdate[0]}\n"
    linhafinal = linha1+linha2+linha3
    return linhafinal
 
def fatoInutil():
    url = "https://useless-facts.sameerkumar.website/api"

    response = requests.request("GET", url).json()

    translator = Translator(to_lang='pt-br')
    traduzido = translator.translate(response['data'])
    
    return (traduzido)

def poemaRandom():
    url1 = "https://poetrydb.org/title"
    response1 = requests.request("GET", url1).json()

    titulo_aleatorio = random.choice(response1['titles'])
    
    url2 = f"https://poetrydb.org/title/{titulo_aleatorio}"

    response2 = requests.request("GET", url2).json()

    tituloPoema = response2[0]['title']
    autorPoema = response2[0]['author']

    poema = ""
    for line in response2[0]['lines']:
        poema += line + "\n"
    
    mensagemFinal = f"Titulo: {tituloPoema}\nAutor(a): {autorPoema}\n\n{poema}"

    return mensagemFinal


@bot.message_handler(commands=['start','help'])
def send_welcome(message):
    bot.reply_to(message,"Oinc Oinc!")

def extract_arg(arg):
    return arg.split()[1:]

@bot.message_handler(commands=['fotinha'])
def sendCat(message):
    request = pigImage()
    bot.send_photo(GROUP_ID,request,caption="Oinc!")

@bot.message_handler(commands=['spike'])
def sendCorgi(message):
    request = corgiImage()
    bot.send_photo(GROUP_ID, request, caption="Auau!")

@bot.message_handler(commands=['covid'])
def sendReport(message):
    request = covidBrazil()
    bot.reply_to(message, request)

@bot.message_handler(commands=['curiosidade'])
def sendFato(message):
    request = fatoInutil()
    bot.reply_to(message, request)

@bot.message_handler(commands=['poeminha'])
def sendPoema(message):
    poema = poemaRandom()
    bot.reply_to(message, poema)

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='YOUR APP NAME HEROKU' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

