from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import json_util
import os
import json

app = Flask(__name__)
CORS(app)  # Omogućava CORS

# Funkcija za konekciju sa bazom po potrebi
def get_db():
    client = MongoClient(
        "mongodb+srv://user1:awd123faw13@cluster0.m9u9j.mongodb.net/test?retryWrites=true&w=majority",
        tlsAllowInvalidCertificates=True,
        connect=False  # Onemogućava trajnu konekciju
    )
    return client['test']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/form2')
def form2():
    return render_template('form2.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    # Dobij podatke sa forme
    data = request.get_json()
    
    # Dobija podatke iz JS-a
    if not data:
        return jsonify({"error": "No data received"}), 400
    l = collection.count_documents({}) + 1  # Brže brojanje
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
