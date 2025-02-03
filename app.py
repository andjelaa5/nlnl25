from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import json_util
import os
import json
import time  # Za merenje vremena

app = Flask(__name__)
CORS(app)

def get_db():
    print("📡 Pokušaj konekcije sa MongoDB...")  # Log pre konekcije
    start_time = time.time()
    client = MongoClient(
        "mongodb+srv://user1:awd123faw13@cluster0.m9u9j.mongodb.net/test?retryWrites=true&w=majority",
        tlsAllowInvalidCertificates=True,
        connect=False
    )
    print(f"✅ Konekcija sa MongoDB uspostavljena za {round(time.time() - start_time, 2)}s")  # Log posle konekcije
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
    print("📥 Primljen zahtev za /submit")  # Log za početak zahteva
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data received"}), 400

    db = get_db()
    collection = db['users']
    
    print("🔢 Brojanje dokumenata...")
    l = collection.estimated_document_count() + 1  # Brže od count_documents
    
    data["id"] = l
    print("💾 Pokušaj upisa podataka u bazu...")  # Log pre insert-a
    start_insert = time.time()
    collection.insert_one(data)
    print(f"✅ Podaci uspešno upisani za {round(time.time() - start_insert, 2)}s")  # Log posle insert-a

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
