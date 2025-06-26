import random
import uuid
from datetime import datetime, timedelta
from faker import Faker
from app import app, db, Konser, Tiket, Pembeli, Transaksi

fake = Faker('id_ID')

def generate_concert_name():
    """Menciptakan nama konser yang unik dan terdengar nyata."""
    parts = {
        "event_type": ["Festival", "Gelar", "Pesta Musik", "Euforia", "Konser Amal", "Malam"],
        "adjective": ["Spektakuler", "Megah", "Intim", "Akustik", "Merdeka", "Nusantara"],
        "noun": ["Nada", "Harmoni", "Melodi", "Bintang", "Senja", "Irama"]
    }
    return f"{random.choice(parts['event_type'])} {random.choice(parts['adjective'])} {random.choice(parts['noun'])} {fake.year()}"

def seed_data():
    """Fungsi utama untuk mengisi database dengan data dummy."""
    with app.app_context():
        print("Menghapus data lama...")
        Transaksi.query.delete()
        Tiket.query.delete()
        Pembeli.query.delete()
        Konser.query.delete()
        db.session.commit()

        # --- MODIFIKASI PEMBUATAN KONSER DENGAN TANGGAL ---
        print("Membuat data Konser...")
        list_konser = []
        concert_names = set()
        while len(list_konser) < 50:
            nama_konser = generate_concert_name()
            if nama_konser not in concert_names:
                
                # Membuat tanggal dan waktu konser acak di masa depan (7 hingga 180 hari dari sekarang)
                future_date = datetime.now().date() + timedelta(days=random.randint(7, 180))
                # Waktu konser acak antara jam 17:00 dan 21:00
                concert_time_str = f"{random.randint(17, 21)}:{random.choice(['00', '30'])}"
                concert_time = datetime.strptime(concert_time_str, "%H:%M").time()
                concert_datetime = datetime.combine(future_date, concert_time)

                konser = Konser(
                    nama=nama_konser,
                    harga=random.randint(150, 1500) * 1000,
                    gambar=None,
                    band=', '.join(fake.words(nb=random.randint(3, 5), unique=True)),
                    deskripsi=fake.paragraph(nb_sentences=3),
                    tanggal_waktu=concert_datetime  # <-- DATA BARU DITAMBAHKAN DI SINI
                )
                list_konser.append(konser)
                concert_names.add(nama_konser)
        db.session.add_all(list_konser)
        db.session.commit()

        print("Membuat data Pembeli...")
        list_pembeli = []
        for _ in range(1000):
            pembeli = Pembeli(
                id=str(uuid.uuid4())[:8].upper(),
                nama=fake.name(),
                email=fake.unique.email(),
                telepon=fake.phone_number()
            )
            list_pembeli.append(pembeli)
        db.session.add_all(list_pembeli)
        db.session.commit()

        print("Membuat data Tiket...")
        list_tiket = []
        all_konser_from_db = Konser.query.all()
        
        global_ticket_counter = 1

        for konser in all_konser_from_db:
            prefix = konser.nama[:3].upper().replace(" ", "")
            for _ in range(1, random.randint(50, 200)):
                nomor_tiket_baru = f"{prefix}{global_ticket_counter:05d}"
                tiket = Tiket(
                    nomor_tiket=nomor_tiket_baru,
                    nama_konser=konser.nama
                )
                list_tiket.append(tiket)
                global_ticket_counter += 1
        
        db.session.add_all(list_tiket)
        db.session.commit()
        
        print("Membuat data Transaksi...")
        tiket_tersedia = Tiket.query.filter_by(status='Tersedia').all()
        random.shuffle(tiket_tersedia)
        
        all_pembeli_from_db = Pembeli.query.all()
        list_transaksi = []
        jumlah_transaksi_untuk_dibuat = min(1000, len(tiket_tersedia))

        for i in range(jumlah_transaksi_untuk_dibuat):
            tiket_untuk_dijual = tiket_tersedia[i]
            pembeli_terpilih = random.choice(all_pembeli_from_db)
            tiket_untuk_dijual.status = 'Terjual'
            
            transaksi = Transaksi(
                id_transaksi=str(uuid.uuid4())[:8].upper(),
                nomor_tiket=tiket_untuk_dijual.nomor_tiket,
                id_pembeli=pembeli_terpilih.id,
                nama_konser=tiket_untuk_dijual.konser.nama,
                tanggal=datetime.now() - timedelta(days=random.randint(1, 365)),
                harga_transaksi=tiket_untuk_dijual.konser.harga
            )
            list_transaksi.append(transaksi)

        db.session.add_all(list_transaksi)
        db.session.commit()

        print(f"\nSEEDING SELESAI!")
        print(f"Total Konser    : {Konser.query.count()}")
        print(f"Total Pembeli   : {Pembeli.query.count()}")
        print(f"Total Tiket     : {Tiket.query.count()}")
        print(f"Total Transaksi : {Transaksi.query.count()}")

if __name__ == '__main__':
    seed_data()