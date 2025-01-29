import csv
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Omogućava CORS

# Putanja do CSV fajla u static folderu
csv_file = os.path.join(app.static_folder, 'podaci.csv')

# Funkcija za čitanje poslednjeg broja korisnika iz CSV fajla
def get_last_user_number():
    try:
        with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            rows = list(reader)
            if rows:
                # Poslednji red (korisnik) u fajlu ima broj korisnika na prvom mestu
                last_user = rows[-1]
                return int(last_user[0])  # Vrati broj korisnika
            else:
                return 0  # Ako CSV fajl je prazan, vrati 0
    except FileNotFoundError:
        return 0  # Ako fajl ne postoji, vraćamo 0

# Funkcija za upisivanje podataka u CSV fajl
def write_to_csv(data):
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(data)  # Dodaj podatke u fajl

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
@app.route('/save_to_csv', methods=['POST'])
def save_to_csv():
    # Uzmi poslednji broj korisnika iz CSV fajla
    user_counter = get_last_user_number() + 1  # Inkrementiraj broj korisnika

    # Dobij podatke sa forme
    data = request.get_json()

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
    zauzet= data['zauzet']
    par= data['zauzet']
    # Pripremi podatke koji se upisuju u CSV (uključujući broj korisnika)
    user_data = [user_counter, ime, prezime, pol, zeljenipol, tiplicnosti, roleModel, zivotnicilj, zanr, pice, hobi, pesma,zauzet,par]

    # Upisivanje podataka u CSV fajl
    write_to_csv(user_data)

    # Vraćanje odgovora sa dodeljenim brojem korisnika
    return jsonify({
        "message": "Podaci su uspešno sačuvani!",
        "broj": user_counter
    })

# Ruta za prikazivanje svih podataka u CSV fajlu (JSON format)
@app.route('/form3')
def form3():
    data = []
    try:
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        pass  # Ako fajl nije pronađen, vraćamo praznu listu

    # Vraćanje podataka u JSON formatu
    return jsonify({"lista": data})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)), debug=True)
