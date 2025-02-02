from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
import threading
import time
import os
import traceback  # Za detaljno logovanje grešaka

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
        print("📥 Primljeni podaci:", data)

        if not data:
            print("⚠️ Nisu primljeni podaci.")
            return jsonify({"error": "Nisu primljeni podaci."}), 400

        # Provera obaveznih polja
        obavezna_polja = ["ime", "prezime", "pol", "zeljenipol", "tiplicnosti", "roleModel"]
        for polje in obavezna_polja:
            if polje not in data or not data[polje]:
                print(f"⚠️ Nedostaje obavezno polje: {polje}")
                return jsonify({"error": f"Nedostaje obavezno polje: {polje}"}), 400

        # Provera MongoDB konekcije
        try:
            client.admin.command('ping')
        except Exception as db_error:
            print("❌ Problem sa konekcijom ka bazi:", db_error)
            return jsonify({"error": "Ne mogu da se povežem sa bazom."}), 500

        # Generisanje ID-ja
        try:
            last_entry = collection.find_one(sort=[("_id", -1)])
            new_id = last_entry["id"] + 1 if last_entry and "id" in last_entry else 1
            data["id"] = new_id
        except Exception as id_error:
            print("❌ Problem sa generisanjem ID-ja:", id_error)
            return jsonify({"error": "Greška prilikom generisanja ID-ja."}), 500

        # Ubacivanje podataka u MongoDB
        try:
            insert_result = collection.insert_one(data)
            print("✅ Podaci sačuvani sa ID:", new_id, "| Mongo ID:", insert_result.inserted_id)
        except Exception as insert_error:
            print("❌ Greška prilikom upisa u bazu:", insert_error)
            return jsonify({"error": "Ne mogu da sačuvam podatke u bazu."}), 500

        return jsonify({
            "message": "Podaci su uspešno sačuvani!",
            "id": new_id
        }), 200

    except Exception as e:
        print("❌ Neuhvaćena greška:", e)
        return jsonify({"error": f"Došlo je do greške na serveru: {str(e)}"}), 500



# Ruta za prikazivanje svih podataka u JSON formatu
@app.route('/get_data', methods=['GET'])
def get_data():
    try:
        data = list(collection.find())
        return jsonify({"data": data}), 200
    except Exception as e:
        print("❌ Greška prilikom preuzimanja podataka:", e)
        traceback.print_exc()
        return jsonify({"error": "Ne mogu da preuzmem podatke."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
