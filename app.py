from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient, errors
from bson import json_util
import os
import json
import time
import threading

app = Flask(__name__)
CORS(app)

# 🔗 Održavanje stalne konekcije sa bazom
try:
    print("📡 [SERVER] Povezivanje sa MongoDB...")
    client = MongoClient(
        "mongodb+srv://user1:awd123faw13@cluster0.m9u9j.mongodb.net/test?retryWrites=true&w=majority",
        tlsAllowInvalidCertificates=True,
        serverSelectionTimeoutMS=5000,   # Timeout za povezivanje
        connectTimeoutMS=5000,           # Timeout za konekciju
        socketTimeoutMS=5000             # Timeout za mrežni soket
    )
    db = client['test']
    collection = db['users']
    client.admin.command('ping')
    print("✅ [SERVER] Konekcija sa MongoDB uspostavljena.")
except errors.ServerSelectionTimeoutError as err:
    print(f"❌ [SERVER] Greška prilikom povezivanja sa bazom: {err}")
    db = None
    collection = None

# 🚀 Periodični ping da se veza ne "uspava"
def keep_connection_alive():
    while True:
        try:
            client.admin.command('ping')
            print("🔄 [KEEP-ALIVE] Ping uspešan.")
        except errors.PyMongoError as e:
            print(f"❌ [KEEP-ALIVE] Greška pri pingovanju: {e}")
        time.sleep(300)  # Ping na svakih 5 minuta

# Pokretanje pingovanja u posebnom thread-u
threading.Thread(target=keep_connection_alive, daemon=True).start()

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
        # Log pre brojanja dokumenata
        start_count = time.time()
        print(f"🔢 [SERVER] Brojanje dokumenata započeto u {start_count}")
        l = collection.estimated_document_count() + 1
        print(f"✅ [SERVER] Brojanje završeno u {time.time()}, trajalo: {round(time.time() - start_count, 2)}s")

        # Log pre insertovanja
        start_insert = time.time()
        print(f"💾 [SERVER] Insert podataka započet u {start_insert}")
        data["id"] = l
        collection.insert_one(data)
        print(f"✅ [SERVER] Insert završen u {time.time()}, trajalo: {round(time.time() - start_insert, 2)}s")

        end_request = time.time()
        print(f"🎯 [SERVER] Završetak obrade zahteva u {end_request}, ukupno trajanje: {round(end_request - start_request, 2)}s")

        return jsonify({
            "message": "Podaci su uspešno sačuvani!",
            "broj": l
        })
    except errors.PyMongoError as e:
        print(f"❌ [SERVER] Greška prilikom upisa u bazu: {e}")
        return jsonify({"error": "Database write error"}), 500

@app.route('/form3')
def form3():
    return render_template('form3.html')

@app.route('/get_form3_data')
def get_form3_data():
    if collection is None:
        return jsonify({"error": "Database connection failed"}), 500

    data_list = list(collection.find())
    return jsonify({"lista": json.loads(json_util.dumps(data_list))})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
