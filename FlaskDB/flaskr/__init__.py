#!/usr/bin/python3
# -*- coding: latin-1 -*-
import os
import sys
# import psycopg2
import json
from bson import json_util
from pymongo import MongoClient
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import pymongo


def create_app():
    app = Flask(__name__)
    return app

app = create_app()

# REPLACE WITH YOUR DATABASE NAME
MONGODATABASE = "grupo26"
MONGOSERVER = "localhost"
MONGOPORT = 27017
client = MongoClient(MONGOSERVER, MONGOPORT)
mongodb = client[MONGODATABASE]

''' # Uncomment for postgres connection
# REPLACE WITH YOUR DATABASE NAME, USER AND PASS
POSTGRESDATABASE = "mydatabase"
POSTGRESUSER = "myuser"
POSTGRESPASS = "mypass"
postgresdb = psycopg2.connect(
    database=POSTGRESDATABASE,
    user=POSTGRESUSER,
    password=POSTGRESPASS)
'''

#Cambiar por Path Absoluto en el servidor
QUERIES_FILENAME = '/var/www/bd/FlaskDB/flaskr/queries'


@app.route("/")
def home():
    with open(QUERIES_FILENAME, 'r', encoding='utf-8') as queries_file:
        json_file = json.load(queries_file)
        pairs = [(x["name"],
                  x["database"],
                  x["description"],
                  x["query"]) for x in json_file]
        return render_template('file.html', results=pairs)

@app.route("/numeros_por_fecha/<string:fecha>")
def numeros_por_fecha(fecha):
    result = list()
    for tupla in mongodb.escuchas.find({"fecha": fecha}, {"_id": 0, "$id": 0, "ciudad": 0, "contenido": 0, "fecha": 0}):
        result.append(tupla)
    return json.dumps(result)

@app.route("/numero_y_entero/<string:numero>/<string:k>")
def numero_y_entero(numero, k):
    #num = request.args.get('k', None)
    contador = 0
    result = list()
    for tupla in mongodb.escuchas.find({"numero": numero}, {"_id": 0, "$id": 0, "ciudad": 0, "fecha": 0, "numero": 0}).sort(
            "fecha", pymongo.ASCENDING):
        result.append(tupla)
        if contador == k:
            break
        contador += 1
    return json.dumps(result)

@app.route("/palabra_clave/<string:palabra>")
def palabra_clave(palabra):
    result = list()
    contador=0
    for tupla in mongodb.escuchas.find({"$text": {"$search": palabra}}, {"_id": 0, "$id": 0}):
        contador+=1
        result.append(tupla)
        if contador == 10:
            break
    return json.dumps(result)


@app.route("/mongo")
def mongo():
    query = request.args.get("query")
    results = eval('mongodb.'+query)
    results = json_util.dumps(results, sort_keys=True, indent=4)
    if "find" in query:
        return render_template('mongo.html', results=results)
    else:
        return "ok"


@app.route("/postgres")
def postgres():
    query = request.args.get("query")
    cursor = postgresdb.cursor()
    cursor.execute(query)
    results = [[a for a in result] for result in cursor]
    print(results)
    return render_template('postgres.html', results=results)


@app.route("/example")
def example():
    return render_template('example.html')


if __name__ == "__main__":
    app.run()
