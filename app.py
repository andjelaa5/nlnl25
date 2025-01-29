from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Omogućava CORS

# Konfiguracija za bazu podataka
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///podaci.db'  # Korišćenje SQLite baze
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Definicija modela za korisnike
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String(100))
    prezime = db.Column(db.String(100))
    pol = db.Column(db.String(10))
    zeljenipol = db.Column(db.String(10))
    tiplicnosti = db.Column(db.String(100))
    roleModel = db.Column(db.String(100))
    zivotnicilj = db.Column(db.String(100))
    zanr = db.Column(db.String(100))
    pice = db.Column(db.String(100))
    hobi = db.Column(db.String(100))
    pesma = db.Column(db.String(100))
    zauzet = db.Column(db.Boolean)
    par = db.Column(db.Integer)  # Povezivanje sa parom

# Koristimo `app.app_context()` da obezbedimo da se pozivi baze izvršavaju u kontekstu aplikacije
with app.app_context():
    db.create_all()  # Kreira bazu podataka ako ne postoji, samo u kontekstu aplikacije

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

@app.route('/form3')
def form3_html():
    return render_template('form3.html')

# Ruta za primanje podataka sa forme i upisivanje u bazu
@app.route('/save_to_csv', methods=['POST'])
def save_to_csv():
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
    zauzet = data['zauzet']
    par = data['zauzet']  # Pretpostavljam da "zauzet" znači da je par

    # Kreiraj korisnika u bazi
    user = User(
        ime=ime, prezime=prezime, pol=pol, zeljenipol=zeljenipol,
        tiplicnosti=tiplicnosti, roleModel=roleModel, zivotnicilj=zivotnicilj,
        zanr=zanr, pice=pice, hobi=hobi, pesma=pesma, zauzet=zauzet, par=par
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Podaci su uspešno sačuvani!"})

# Ruta za prikazivanje svih podataka u bazi (JSON format)
@app.route('/get_form3_data')
def form3_data():
    users = User.query.all()
    data = []
    for user in users:
        data.append({
            "id": user.id, "ime": user.ime, "prezime": user.prezime,
            "pol": user.pol, "zeljenipol": user.zeljenipol, "tiplicnosti": user.tiplicnosti,
            "roleModel": user.roleModel, "zivotnicilj": user.zivotnicilj,
            "zanr": user.zanr, "pice": user.pice, "hobi": user.hobi,
            "pesma": user.pesma, "zauzet": user.zauzet, "par": user.par
        })

    return jsonify({"lista": data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
