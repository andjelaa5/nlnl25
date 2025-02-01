import csv
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import pandas as pd
import json
from bson import json_util 
import os
import threading
import time

app = Flask(__name__)
CORS(app)  # Omogućava CORS

client = MongoClient(
    "mongodb+srv://user1:awd123faw13@cluster0.m9u9j.mongodb.net/test?retryWrites=true&w=majority",
    tlsAllowInvalidCertificates=True
)

def ping_mongo():
    while True:
        try:
           client.admin.command('ping')  # Ping za proveru konekcije
           print("Konekcija je aktivna.")
        except Exception as e:
            print("Greška sa konekcijom:", e)
        time.sleep(60)  # Ping svakih 5 minuta

# Pokreće ping u pozadini
threading.Thread(target=ping_mongo, daemon=True).start()

db = client['test']
collection = db['users']  # Ime kolekcije
#result = collection.delete_many({}) 
# Putanja do CSV fajla (proveri da li je fajl na pravoj lokaciji)

# Ruta za serviranje HTML forme
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form')
def form():
    return render_template('form.html')


@app.route('/form2')
def form2():
    return render_template('form2.html')
# Ruta za primanje podataka sa forme i upisivanje u CSV
@app.route('/submit', methods=['POST'])
def submit_form():
    # Dobij podatke sa forme
    data = request.get_json()
    # Dobija podatke iz JS-a
    if not data:
        return jsonify({"error": "No data received"}), 400
    gas = list(collection.find())
    # Ubacivanje u MongoDB
    l = len(gas) + 1
    ime = data['ime']
    prezime = data['prezime']
    pol = data['pol']
    zeljenipol = data['zeljenipol']
    tiplicnosti = data['tiplicnosti']
    roleModel = data['roleModel']
    zivotnicilj = data['zivotnicilj']
    zanr = data['zanr']
    pice = data['pice']
    hobi = data['hobi']
    pesma = data['pesma']
    zauzet = data['zauzet']
    par = data['zauzet']
    user_data = [l, ime, prezime, pol, zeljenipol, tiplicnosti, roleModel, zivotnicilj, zanr, pice, hobi, pesma, zauzet, par]
    data["id"] = l
    collection.insert_one(data)
    return jsonify({
        "message": "Podaci su uspešno sačuvani!",
        "broj": l
    })

# Ruta za prikazivanje svih podataka u CSV fajlu (JSON format)
@app.route('/form3')
def form3():
    return render_template('form3.html')

@app.route('/get_form3_data')
def get_form3_data():
    gas = list(collection.find())
    return jsonify({"lista": json.loads(json_util.dumps(gas))})
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
