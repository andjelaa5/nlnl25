import csv
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient, errors
import json
from bson import json_util 
import os
import threading
import time

app = Flask(__name__)
CORS(app)  # Omogućava CORS

client = MongoClient(
    "mongodb+srv://user1:awd123faw13@cluster0.m9u9j.mongodb.net/test?retryWrites=true&w=majority",
    tlsAllowInvalidCertificates=True,
    serverSelectionTimeoutMS=5000,   # Timeout za povezivanje (5s)
    connectTimeoutMS=5000,           # Timeout za konekciju (5s)
    socketTimeoutMS=5000             # Timeout za mrežni soket (5s)
)
db = client['test']
collection = db['users']  # Ime kolekcije

# Ruta za testiranje pinga ka MongoDB
@app.route('/test_ping')
def test_ping():
    try:
        start_ping = time.time()
        client.admin.command('ping')
        duration = round(time.time() - start_ping, 2)
        return jsonify({"message": "Ping uspešan", "trajanje": duration})
    except errors.PyMongoError as e:
        return jsonify({"error": str(e)}), 500

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

# Ruta za primanje podataka sa forme i upisivanje u MongoDB
@app.route('/submit', methods=['POST'])
def submit_form():
    start_request = time.time()
    print(f"📥 [SERVER] Primljen zahtev za /submit u {start_request}")

    data = request.get_json()

    if not data:
        print("⚠️ [SERVER] Nisu primljeni podaci.")
        return jsonify({"error": "No data received"}), 400

    if collection is None:
        print("❌ [SERVER] Nema konekcije sa bazom.")
        return jsonify({"error": "Database connection failed"}), 500

    try:
        # Testiraj ping ka bazi
        print("🔄 [SERVER] Ping ka bazi pre brojanja...")
        client.admin.command('ping')  
        print("✅ [SERVER] Ping uspešan.")

        # Brojanje dokumenata
        start_count = time.time()
        print(f"🔢 [SERVER] Početak brojanja dokumenata u {start_count}")
        l = collection.estimated_document_count() + 1
        print(f"✅ [SERVER] Završeno brojanje u {time.time()}, trajanje: {round(time.time() - start_count, 2)}s")

        # Insert podataka
        start_insert = time.time()
        print(f"💾 [SERVER] Početak insertovanja u {start_insert}")
        data["id"] = l
        collection.insert_one(data)
        print(f"✅ [SERVER] Insert završen u {time.time()}, trajanje: {round(time.time() - start_insert, 2)}s")

        end_request = time.time()
        print(f"🎯 [SERVER] Završetak obrade u {end_request}, ukupno trajanje: {round(end_request - start_request, 2)}s")

        return jsonify({
            "message": "Podaci su uspešno sačuvani!",
            "broj": l
        })
    except errors.PyMongoError as e:
        print(f"❌ [SERVER] Greška sa bazom: {e}")
        return jsonify({"error": "Database write error"}), 500

# Ruta za prikazivanje svih podataka u MongoDB (JSON format)
@app.route('/form3')
def form3():
    return render_template('form3.html')

@app.route('/get_form3_data')
def get_form3_data():
    gas = list(collection.find())
    return jsonify({"lista": json.loads(json_util.dumps(gas))})
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
