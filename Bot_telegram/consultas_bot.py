import telebot
import numpy as np
import os
import json
from elasticsearch import Elasticsearch

TOKEN = "5272407579:AAHU10YpHKTgIkE7bcZmviOeMwGy92fk8ig"

bot = telebot.TeleBot(TOKEN)

es= Elasticsearch(hosts='https://localhost:9200',basic_auth=('elastic','tv_pJkdqoCKde*VYQ4c2'),ca_certs='/home/alvaro/elasticsearch-8.1.3/config/certs/http_ca.crt')


@bot.message_handler(commands=['comandos'])
def send_welcome(message):
    print(message)
    response=str("count, first, last, media_temperatura_ambiente, media_temperatura_horno, valores_mayor_media_temperatura_menor_media_horno, max_humedad, min_humedad")
    bot.reply_to(message, response)



@bot.message_handler(commands=['count'])
def count_documents(message):
    x= message.text.split()
    indice=x[1]
    print(indice)
    response=es.count(index=indice)
    print(response)
    bot.reply_to(message, "Numero de documentos indexados en"+indice+': '+str(response['count']))



@bot.message_handler(commands=['last'])
def query_last_document(message):
    x= message.text.split()
    print(x)
    
    indice=x[1]
    response=str(es.search(index=indice,query={"match_all":{}},size=1,sort={"@timestamp":'desc'}))
    print(response)
    bot.reply_to(message,"Ultimo documento indexado en "+indice+': '+response)

@bot.message_handler(commands=['first'])
def query_first_document(message):
    x= message.text.split()
    indice=x[1]
    response=str(es.search(index=indice,query={"match_all":{}},size=1,sort={"@timestamp":'asc'}))
    bot.reply_to(message,"Primer documento indexado en "+indice+': '+response)

@bot.message_handler(commands=['media_temperatura_ambiente'])
def query_average_temp_amb_document(message):
    x= message.text.split()
    indice=x[1]
    response=es.search(index=indice,aggs= {  "avg_temp_ambiente": { "avg": { "field": "TEMP_AMBIENTE" }}})["aggregations"]["avg_temp_ambiente"]["value"]
    print('response')
    print(response)
    bot.reply_to(message,"Media de temperatura ambiente en "+indice+': '+str(response))

@bot.message_handler(commands=['media_temperatura_horno'])
def query_average_temp_horno_document(message):
    x= message.text.split()
    indice=x[1]
    response=es.search(index=indice,aggs= {  "avg_temp_horno": { "avg": { "field": "TEMP_HORNO" }}})["aggregations"]["avg_temp_horno"]["value"]
    bot.reply_to(message,"Media de temperatura del horno en  "+indice+': '+str(response))


@bot.message_handler(commands=['valores_mayor_media_temperatura_menor_media_horno'])
def query_conditions_document(message):
    x= message.text.split()
    indice=x[1]
    valor1=es.search(index=indice, aggs= {  "avg_temp_ambiente": { "avg": { "field": "TEMP_AMBIENTE" }}})["aggregations"]["avg_temp_ambiente"]["value"]
    valor2=es.search(index=indice, aggs= {  "avg_temp_horno": { "avg": { "field": "TEMP_HORNO" }}})["aggregations"]["avg_temp_horno"]["value"]
    response=es.search(index=indice,query={"bool":{"must":[{"range":{"TEMP_AMBIENTE":{"gte":valor1}}},{"range":{"TEMP_HORNO":{"lte":valor2}}}]}})
    bot.reply_to(message,"Valores que tengan mas que la media de temperatura ambiente y menos de la media que la temperatura del horno en "+indice+': '+str(response))



@bot.message_handler(commands=['max_humedad'])
def query_max_humidity_document(message):
    x= message.text.split()
    indice=x[1]
    response=es.search(index=indice,aggs= {"max_humidity": { "max": { "field": "HUMEDAD" }}})["aggregations"]["max_humidity"]["value"]
    bot.reply_to(message,"Maximo valor de humedad en "+indice+': '+str(response))

@bot.message_handler(commands=['min_humedad'])
def query_min_humidity_document(message):
    x= message.text.split()
    indice=x[1]
    response=es.search(index=indice,aggs= {"min_humidity": { "min": { "field": "HUMEDAD" }}})["aggregations"]["min_humidity"]["value"]
    bot.reply_to(message,"Minimo valor de humedad en "+indice+': '+str(response))

bot.polling()

