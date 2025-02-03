import csv
from flask import Flask, render_template, request, jsonify, g
from flask_cors import CORS
from pymongo import MongoClient
import pandas as pd
import json
from bson import json_util 
import os

app = Flask(__name__)
CORS(app)  # Omogućava CORS

# Funkcija za uspostavljanje konekcije sa bazom
def get_db():
    if 'db' not in g:
        client = MongoClient(
            "mongodb+srv://user1:awd123faw13@cluster0.m9u9j.mongodb.net/test?retryWrites=true&w=majority",
            tlsAllowInvalidCertificates=True,
            socketKeepAlive=True  # Održava aktivnu konekciju
        )
        g.client = client
        g.db = client['test']
    return g.db

# Zatvaranje konekcije na kraju svakog zahteva
@app.teardown_appcontext
def close_db(error):
    client = g.pop('client', None)
    if client is not None:
        client.close()

# Ping pre svakog zahteva (provera da li je konekcija aktivna)
@app.before_request
def keep_connection_alive():
    try:
        db = get_db()
        db.command('ping')
    except:
        g.pop('db', None)  # Ako je konekcija prekinuta, resetuj

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

# Ruta za primanje podataka sa forme i upisivanje u bazu
@app.route('/submit', methods=['POST'])
def submit_form():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data received"}), 400

    db = get_db()
    collection = db['users']
    
    # Optimizovano brojanje dokumenata
    l = collection.estimated_document_count() + 1

    data["id"] = l
    collection.insert_one(data)
    
    return jsonify({
        "message": "Podaci su uspešno sačuvani!",
        "broj": l
    })

# Ruta za prikazivanje svih podataka
@app.route('/form3')
def form3():
    return render_template('form3.html')

@app.route('/get_form3_data')
def get_form3_data():
    db = get_db()
    collection = db['users']
    data_list = list(collection.find())
    return jsonify({"lista": json.loads(json_util.dumps(data_list))})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
