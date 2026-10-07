import os

# Isi sesuai database di container "db" (atau set lewat environment variable)
DB_HOST = os.environ.get("DB_HOST", "IP_CONTAINER_DB")
DB_USER = os.environ.get("DB_USER", "userapp")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "passwordkamu")
DB_NAME = os.environ.get("DB_NAME", "ukt_db")

# DATABASE_URL hanya untuk testing lokal (misal sqlite), biarkan kosong di praktikum
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

# Label pilihan form. Kunci = kode di dataset. Ubah teksnya sesuai arti kode di datasetmu.
LABEL_STATUS_ORTU = {1: "Kode 1", 2: "Kode 2", 4: "Kode 4"}
LABEL_RUMAH = {1: "Kode 1", 0: "Kode 0"}
LABEL_DAYA_LISTRIK = {1: "Kode 1", 2: "Kode 2", 3: "Kode 3"}
