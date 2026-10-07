import os
from datetime import datetime

import joblib
import pandas as pd
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

import config
from train_model import FITUR, train

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)

MODEL_PATH = "model.pkl"
model = joblib.load(MODEL_PATH) if os.path.exists(MODEL_PATH) else train(out=MODEL_PATH)


class Prediksi(db.Model):
    __tablename__ = "prediksi"
    id = db.Column(db.Integer, primary_key=True)
    status_ortu = db.Column(db.Integer, nullable=False)
    penghasilan = db.Column(db.Integer, nullable=False)
    status_rumah = db.Column(db.Integer, nullable=False)
    jml_motor = db.Column(db.Integer, nullable=False)
    jml_mobil = db.Column(db.Integer, nullable=False)
    daya_listrik = db.Column(db.Integer, nullable=False)
    hasil = db.Column(db.String(40), nullable=False)
    probabilitas = db.Column(db.Float, nullable=False)
    waktu = db.Column(db.DateTime, default=datetime.now)


with app.app_context():
    db.create_all()


def form_context(**extra):
    return dict(status_ortu=config.LABEL_STATUS_ORTU, rumah=config.LABEL_RUMAH,
                listrik=config.LABEL_DAYA_LISTRIK, **extra)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html", **form_context(hasil=None, error=None, nilai={}))

    nilai = request.form.to_dict()
    try:
        data = [int(nilai[f]) for f in FITUR]
        if min(data) < 0:
            raise ValueError
    except (KeyError, ValueError):
        return render_template("index.html", **form_context(
            hasil=None, nilai=nilai, error="Semua kolom wajib diisi dengan angka 0 atau lebih.")), 400

    proba = float(model.predict_proba(pd.DataFrame([data], columns=FITUR))[0][1])
    label = "Berpotensi KIP-K" if proba >= 0.5 else "Tidak berpotensi KIP-K"
    db.session.add(Prediksi(status_ortu=data[0], penghasilan=data[1], status_rumah=data[2],
                            jml_motor=data[3], jml_mobil=data[4], daya_listrik=data[5],
                            hasil=label, probabilitas=proba))
    db.session.commit()
    return render_template("index.html", **form_context(
        hasil={"label": label, "persen": round(proba * 100, 1), "layak": proba >= 0.5},
        nilai=nilai, error=None))


@app.route("/riwayat")
def riwayat():
    rows = Prediksi.query.order_by(Prediksi.id.desc()).limit(100).all()
    return render_template("riwayat.html", rows=rows)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
