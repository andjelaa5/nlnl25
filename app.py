from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
import threading
import time
import os

app = Flask(__name__)
CORS(app)  # Omogućava CORS za frontend

# Konekcija sa MongoDB
client = MongoClient(
    "mongodb+srv://user1:awd123faw13@cluster0.m9u9j.mongodb.net/test?retryWrites=true&w=majority",
    tlsAllowInvalidCertificates=True,
    maxPoolSize=100,
    minPoolSize=10
)

db = client['test']
collection = db['users']

# Funkcija za periodično proveravanje konekcije sa bazom
def ping_mongo():
    while True:
        try:
            client.admin.command('ping')
            print("✅ Konekcija sa MongoDB je aktivna.")
        except Exception as e:
            print("⚠️ Greška sa konekcijom:", e)
        time.sleep(60)  # Ping svakih 60 sekundi

# Pokreće ping u pozadini
threading.Thread(target=ping_mongo, daemon=True).start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/form2')
def form2():
    return render_template('form2.html')

@app.route('/form3')
def form3():
    return render_template('form3.html')

# Ruta za primanje podataka sa forme i upisivanje u MongoDB
@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Nisu primljeni podaci."}), 400

        # Automatsko generisanje ID
        last_entry = collection.find_one(sort=[("id", -1)])
        new_id = last_entry["id"] + 1 if last_entry and "id" in last_entry else 1
        data["id"] = new_id

        # Ubacivanje podataka u MongoDB
        collection.insert_one(data)

        return jsonify({
            "message": "Podaci su uspešno sačuvani!",
            "id": new_id
        }), 200

    except Exception as e:
        print("❌ Server Error:", e)
        return jsonify({"error": "Došlo je do greške na serveru."}), 500

# Ruta za prikazivanje svih podataka u JSON formatu
@app.route('/get_data', methods=['GET'])
def get_data():
    try:
        data = list(collection.find())
        return jsonify({"data": data}), 200
    except Exception as e:
        print("❌ Greška prilikom preuzimanja podataka:", e)
        return jsonify({"error": "Ne mogu da preuzmem podatke."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
