from flask import Flask, render_template, request, redirect, url_for, flash
import uuid
import os
from werkzeug.utils import secure_filename
import datetime
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload

# Inisialisasi Aplikasi Flask
app = Flask(__name__)
app.secret_key = 'kunci_rahasia_anda_yang_sangat_aman'

# Konfigurasi dari file .env dan Database
load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+pymysql://root:@localhost/db_konser_tiket')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Konfigurasi Folder Upload
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """Fungsi untuk memeriksa ekstensi file yang diizinkan."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# --- MODEL DATABASE (Struktur tidak diubah) ---
class Konser(db.Model):
    __tablename__ = 'konser'
    nama = db.Column(db.String(100), primary_key=True)
    harga = db.Column(db.Integer, nullable=False)
    gambar = db.Column(db.String(255))
    band = db.Column(db.Text)
    deskripsi = db.Column(db.Text)
    tanggal_waktu = db.Column(db.DateTime, nullable=True)
    tiket = db.relationship('Tiket', backref='konser', lazy=True, cascade="all, delete-orphan")

class Pembeli(db.Model):
    __tablename__ = 'pembeli'
    id = db.Column(db.String(8), primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    telepon = db.Column(db.String(20))

class Tiket(db.Model):
    __tablename__ = 'tiket'
    nomor_tiket = db.Column(db.String(10), primary_key=True)
    nama_konser = db.Column(db.String(100), db.ForeignKey('konser.nama', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    status = db.Column(db.Enum('Tersedia', 'Terjual'), nullable=False, default='Tersedia')
    transaksi = db.relationship('Transaksi', backref='detail_tiket', lazy=True, cascade="all, delete-orphan", uselist=False)

class Transaksi(db.Model):
    __tablename__ = 'transaksi'
    id_transaksi = db.Column(db.String(8), primary_key=True)
    nomor_tiket = db.Column(db.String(10), db.ForeignKey('tiket.nomor_tiket'), unique=True)
    id_pembeli = db.Column(db.String(8), db.ForeignKey('pembeli.id'))
    nama_konser = db.Column(db.String(100))
    tanggal = db.Column(db.Date, nullable=False)
    harga_transaksi = db.Column(db.Integer, nullable=False)
    pembeli = db.relationship('Pembeli', backref='transaksi', lazy=True)


# --- IMPLEMENTASI STRUKTUR DATA & ALGORITMA MANUAL ---

# 1. Implementasi Linked List Manual
class Node:
    """Kelas untuk merepresentasikan satu elemen (node) dalam Linked List."""
    def __init__(self, data_yang_disimpan):
        self.data = data_yang_disimpan  # Data yang disimpan (misal: objek Konser)
        self.node_berikutnya = None  # Pointer ke node berikutnya

class LinkedList:
    """Kelas untuk mengelola operasi pada Linked List."""
    def __init__(self):
        self.head_node = None  # Node pertama dalam list

    def append(self, data_baru):
        """Menambahkan node baru di akhir list."""
        node_baru = Node(data_baru)
        if self.head_node is None:
            self.head_node = node_baru
            return
        
        node_terakhir = self.head_node
        while node_terakhir.node_berikutnya:
            node_terakhir = node_terakhir.node_berikutnya
        node_terakhir.node_berikutnya = node_baru

    def to_list(self):
        """Mengubah Linked List kembali menjadi Python List biasa agar mudah digunakan."""
        list_hasil = []
        node_sekarang = self.head_node
        while node_sekarang:
            list_hasil.append(node_sekarang.data)
            node_sekarang = node_sekarang.node_berikutnya
        return list_hasil

# 2. Implementasi Merge Sort Manual
def merge_sort(array_input, key_untuk_sort=lambda item: item, urutkan_terbalik=False):
    """
    Fungsi untuk mengurutkan sebuah list menggunakan algoritma Merge Sort.
    Mendukung pengurutan terbalik (descending).
    """
    panjang_array = len(array_input)
    if panjang_array > 1:
        # --- Fase Pembagian (Divide) ---
        indeks_tengah = panjang_array // 2
        bagian_kiri = array_input[:indeks_tengah]
        bagian_kanan = array_input[indeks_tengah:]
        
        # Panggil rekursif untuk setiap bagian
        merge_sort(bagian_kiri, key_untuk_sort, urutkan_terbalik)
        merge_sort(bagian_kanan, key_untuk_sort, urutkan_terbalik)
        
        # --- Fase Penggabungan (Conquer) ---
        indeks_kiri, indeks_kanan, indeks_gabungan = 0, 0, 0
        
        while indeks_kiri < len(bagian_kiri) and indeks_kanan < len(bagian_kanan):
            # Tentukan kondisi berdasarkan flag 'urutkan_terbalik'
            if urutkan_terbalik:
                # Untuk descending, masukkan elemen yang lebih besar lebih dulu
                kondisi = key_untuk_sort(bagian_kiri[indeks_kiri]) > key_untuk_sort(bagian_kanan[indeks_kanan])
            else:
                # Untuk ascending, masukkan elemen yang lebih kecil lebih dulu
                kondisi = key_untuk_sort(bagian_kiri[indeks_kiri]) < key_untuk_sort(bagian_kanan[indeks_kanan])
            
            if kondisi:
                array_input[indeks_gabungan] = bagian_kiri[indeks_kiri]
                indeks_kiri += 1
            else:
                array_input[indeks_gabungan] = bagian_kanan[indeks_kanan]
                indeks_kanan += 1
            indeks_gabungan += 1

        # Salin sisa elemen jika ada dari bagian kiri
        while indeks_kiri < len(bagian_kiri):
            array_input[indeks_gabungan] = bagian_kiri[indeks_kiri]
            indeks_kiri += 1
            indeks_gabungan += 1
        
        # Salin sisa elemen jika ada dari bagian kanan
        while indeks_kanan < len(bagian_kanan):
            array_input[indeks_gabungan] = bagian_kanan[indeks_kanan]
            indeks_kanan += 1
            indeks_gabungan += 1
    return array_input


# --- FUNGSI-FUNGSI APLIKASI (ROUTES) DENGAN IMPLEMENTASI PENUH ---

@app.route('/')
def home():
    search_query = request.args.get('search_query', '').lower()
    
    semua_konser_dari_db = Konser.query.all()
    konser_mendatang_list = [konser for konser in semua_konser_dari_db if konser.tanggal_waktu and konser.tanggal_waktu > datetime.datetime.now()]

    if search_query:
        # Ini adalah implementasi Linear Search
        konser_hasil_filter = [konser for konser in konser_mendatang_list if search_query in konser.nama.lower() or search_query in konser.band.lower() or search_query in konser.deskripsi.lower()]
    else:
        konser_hasil_filter = konser_mendatang_list

    konser_linked_list = LinkedList()
    for item_konser in konser_hasil_filter:
        konser_linked_list.append(item_konser)
    
    konser_untuk_diurutkan = konser_linked_list.to_list()
    
    konser_terurut = merge_sort(konser_untuk_diurutkan, key_untuk_sort=lambda konser: konser.tanggal_waktu)
    
    konser_untuk_ditampilkan = konser_terurut[:3] if not search_query else konser_terurut
    konser_unggulan = konser_terurut[0] if konser_terurut else None

    return render_template(
        'home.html', 
        upcoming_konser=konser_untuk_ditampilkan,
        featured_konser=konser_unggulan,
        search_query=request.args.get('search_query', '')
    )

@app.route('/beli-tiket/<string:nama_konser>')
def beli_tiket_page(nama_konser):
    konser = Konser.query.get_or_404(nama_konser)
    list_tiket_tersedia = Tiket.query.filter_by(nama_konser=nama_konser, status='Tersedia').all()
    jumlah_tiket_tersedia = len(list_tiket_tersedia)
    return render_template('beli_tiket.html', konser=konser, jumlah_tiket_tersedia=jumlah_tiket_tersedia)

@app.route('/proses-pembelian', methods=['POST'])
def proses_pembelian():
    # NOTE: Fungsi ini tidak diubah karena `with_for_update()` adalah operasi
    # database yang kritikal untuk mencegah race condition.
    nama_konser = request.form.get('nama_konser')
    nama_pembeli = request.form.get('nama_pembeli')
    email_pembeli = request.form.get('email_pembeli')
    telepon_pembeli = request.form.get('telepon_pembeli')
    tiket_untuk_dijual = Tiket.query.filter_by(nama_konser=nama_konser, status='Tersedia').with_for_update().first()
    if not tiket_untuk_dijual:
        flash('Maaf, tiket untuk konser ini baru saja habis!', 'error')
        return redirect(url_for('home'))
    pembeli = Pembeli.query.filter_by(email=email_pembeli).first()
    if not pembeli:
        pembeli = Pembeli(id=str(uuid.uuid4())[:8].upper(), nama=nama_pembeli, email=email_pembeli, telepon=telepon_pembeli)
        db.session.add(pembeli)
        flash(f'Selamat datang, {nama_pembeli}! Akun Anda telah dibuat.', 'info')
    else:
        flash(f'Selamat datang kembali, {pembeli.nama}! Transaksi Anda menggunakan data yang sudah ada.', 'info')
    tiket_untuk_dijual.status = 'Terjual'
    transaksi_baru = Transaksi(id_transaksi=str(uuid.uuid4())[:8].upper(), nomor_tiket=tiket_untuk_dijual.nomor_tiket, id_pembeli=pembeli.id, nama_konser=nama_konser, tanggal=datetime.date.today(), harga_transaksi=tiket_untuk_dijual.konser.harga)
    db.session.add(transaksi_baru)
    db.session.commit()
    flash('Pembelian tiket berhasil!', 'success')
    return redirect(url_for('pembelian_sukses', id_transaksi=transaksi_baru.id_transaksi))

@app.route('/pembelian-sukses/<string:id_transaksi>')
def pembelian_sukses(id_transaksi):
    transaksi = Transaksi.query.get_or_404(id_transaksi)
    return render_template('sukses.html', transaksi=transaksi)

@app.route('/dashboard')
def dashboard():
    jumlah_tiket = len(Tiket.query.all())
    jumlah_konser = len(Konser.query.all())
    jumlah_pembeli = len(Pembeli.query.all())
    jumlah_transaksi = len(Transaksi.query.all())
    return render_template('dashboard.html', jumlah_tiket=jumlah_tiket, jumlah_konser=jumlah_konser, jumlah_pembeli=jumlah_pembeli, jumlah_transaksi=jumlah_transaksi)

@app.route('/tiket')
def kelola_tiket():
    sort_by = request.args.get('sort_by', 'nomor')
    semua_tiket = Tiket.query.options(joinedload(Tiket.konser)).all()
    
    tiket_linked_list = LinkedList()
    for item_tiket in semua_tiket:
        tiket_linked_list.append(item_tiket)
    
    tiket_untuk_diurutkan = tiket_linked_list.to_list()

    if sort_by == 'harga_asc':
        tiket_terurut = merge_sort(tiket_untuk_diurutkan, key_untuk_sort=lambda tiket: tiket.konser.harga)
    elif sort_by == 'harga_desc':
        tiket_terurut = merge_sort(tiket_untuk_diurutkan, key_untuk_sort=lambda tiket: tiket.konser.harga, urutkan_terbalik=True)
    else:
        tiket_terurut = merge_sort(tiket_untuk_diurutkan, key_untuk_sort=lambda tiket: tiket.nomor_tiket)
        
    opsi_konser = Konser.query.all()
    return render_template('tiket.html', tickets=tiket_terurut, konser_options=opsi_konser)

@app.route('/tiket/tambah', methods=['POST'])
def tambah_tiket():
    nomor_tiket = request.form['nomor_tiket']
    if Tiket.query.get(nomor_tiket):
        flash('Gagal: Nomor Tiket sudah ada!', 'error')
    else:
        tiket_baru = Tiket(nomor_tiket=nomor_tiket, nama_konser=request.form['nama_konser'], status=request.form['status'])
        db.session.add(tiket_baru)
        db.session.commit()
        flash('Tiket berhasil ditambahkan!', 'success')
    return redirect(url_for('kelola_tiket'))

@app.route('/tiket/edit/<string:nomor_tiket>', methods=['GET', 'POST'])
def edit_tiket(nomor_tiket):
    tiket_yang_diedit = Tiket.query.get_or_404(nomor_tiket)
    if request.method == 'POST':
        tiket_yang_diedit.nama_konser = request.form['nama_konser']
        tiket_yang_diedit.status = request.form['status']
        db.session.commit()
        flash('Tiket berhasil diperbarui!', 'success')
        return redirect(url_for('kelola_tiket'))
    opsi_konser = Konser.query.all()
    return render_template('edit_tiket.html', ticket=tiket_yang_diedit, konser_options=opsi_konser)

@app.route('/tiket/hapus/<string:nomor_tiket>', methods=['POST'])
def hapus_tiket(nomor_tiket):
    tiket_yang_dihapus = Tiket.query.get(nomor_tiket)
    if tiket_yang_dihapus:
        db.session.delete(tiket_yang_dihapus)
        db.session.commit()
        flash('Tiket berhasil dihapus!', 'success')
    else:
        flash('Tiket tidak ditemukan!', 'error')
    return redirect(url_for('kelola_tiket'))

@app.route('/konser')
def kelola_konser():
    semua_data_konser = Konser.query.all()
    
    konser_linked_list = LinkedList()
    for item_konser in semua_data_konser:
        konser_linked_list.append(item_konser)
    
    konser_untuk_diurutkan = konser_linked_list.to_list()
    
    # Gunakan tuple pada key untuk menangani None (konser tanpa tanggal) dengan aman
    konser_terurut = merge_sort(konser_untuk_diurutkan, key_untuk_sort=lambda konser: (konser.tanggal_waktu is not None, konser.tanggal_waktu), urutkan_terbalik=True)
    
    return render_template('konser.html', konser=konser_terurut, search_active=False)

@app.route('/konser/tambah', methods=['POST'])
def tambah_konser():
    nama_konser = request.form.get('nama_konser')
    if Konser.query.get(nama_konser):
        flash('Gagal: Konser dengan nama tersebut sudah ada!', 'error')
        return redirect(url_for('kelola_konser'))
    file = request.files.get('gambar')
    if not file or file.filename == '':
        flash('File gambar wajib diupload!', 'error')
        return redirect(url_for('kelola_konser'))
    tanggal_str = request.form.get('tanggal_waktu')
    objek_tanggal = None
    if tanggal_str:
        try:
            objek_tanggal = datetime.datetime.strptime(tanggal_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            flash('Format tanggal tidak valid.', 'error')
            return redirect(url_for('kelola_konser'))
    if file and allowed_file(file.filename):
        nama_file = secure_filename(file.filename)
        nama_file_unik = str(uuid.uuid4()) + '.' + nama_file.rsplit('.', 1)[1].lower()
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], nama_file_unik))
        konser_baru = Konser(nama=nama_konser, harga=int(request.form.get('harga', 0)), band=request.form.get('band', ''), deskripsi=request.form.get('deskripsi', ''), gambar=nama_file_unik, tanggal_waktu=objek_tanggal)
        db.session.add(konser_baru)
        db.session.commit()
        flash('Konser berhasil ditambahkan!', 'success')
    else:
        flash('Ekstensi file tidak diizinkan!', 'error')
    return redirect(url_for('kelola_konser'))

@app.route('/konser/edit/<string:nama_konser_lama>', methods=['GET', 'POST'])
def edit_konser(nama_konser_lama):
    konser_yang_diedit = Konser.query.get_or_404(nama_konser_lama)
    if request.method == 'POST':
        gambar_lama = konser_yang_diedit.gambar
        konser_yang_diedit.harga = int(request.form.get('harga', 0))
        konser_yang_diedit.band = request.form.get('band', '')
        konser_yang_diedit.deskripsi = request.form.get('deskripsi', '')
        tanggal_str = request.form.get('tanggal_waktu')
        if tanggal_str:
            try:
                konser_yang_diedit.tanggal_waktu = datetime.datetime.strptime(tanggal_str, '%Y-%m-%dT%H:%M')
            except ValueError:
                flash('Format tanggal tidak valid. Perubahan tanggal diabaikan.', 'warning')
        else:
            konser_yang_diedit.tanggal_waktu = None
        file_baru = request.files.get('gambar')
        if file_baru and file_baru.filename != '':
            if allowed_file(file_baru.filename):
                if gambar_lama and os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], gambar_lama)):
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], gambar_lama))
                nama_file = secure_filename(file_baru.filename)
                nama_file_unik = str(uuid.uuid4()) + '.' + nama_file.rsplit('.', 1)[1].lower()
                file_baru.save(os.path.join(app.config['UPLOAD_FOLDER'], nama_file_unik))
                konser_yang_diedit.gambar = nama_file_unik
            else:
                flash('Ekstensi file gambar baru tidak diizinkan! Gambar tidak diubah.', 'warning')
        nama_konser_baru = request.form.get('nama_konser_baru', nama_konser_lama)
        if nama_konser_baru != nama_konser_lama:
            if Konser.query.get(nama_konser_baru):
                flash('Gagal: Nama konser baru sudah ada!', 'error')
                return redirect(url_for('edit_konser', nama_konser_lama=nama_konser_lama))
            konser_yang_diedit.nama = nama_konser_baru
        db.session.commit()
        flash('Konser berhasil diperbarui!', 'success')
        return redirect(url_for('kelola_konser'))
    return render_template('edit_konser.html', konser=konser_yang_diedit)

@app.route('/konser/hapus/<string:nama_konser>', methods=['POST'])
def hapus_konser(nama_konser):
    konser_yang_dihapus = Konser.query.get(nama_konser)
    if konser_yang_dihapus:
        if konser_yang_dihapus.gambar:
            path_file_gambar = os.path.join(app.config['UPLOAD_FOLDER'], konser_yang_dihapus.gambar)
            if os.path.exists(path_file_gambar):
                os.remove(path_file_gambar)
        db.session.delete(konser_yang_dihapus)
        db.session.commit()
        flash('Konser dan semua tiket terkait berhasil dihapus!', 'success')
    else:
        flash('Konser tidak ditemukan!', 'error')
    return redirect(url_for('kelola_konser'))

@app.route('/cari_konser', methods=['POST'])
def cari_konser():
    query = request.form.get('query_konser', '').lower()
    semua_konser = Konser.query.all()
    list_hasil_pencarian = [konser for konser in semua_konser if query in konser.nama.lower()]
    
    hasil_pencarian_linked_list = LinkedList()
    for item_hasil in list_hasil_pencarian:
        hasil_pencarian_linked_list.append(item_hasil)
    
    hasil_pencarian_untuk_ditampilkan = hasil_pencarian_linked_list.to_list()
    
    if not hasil_pencarian_untuk_ditampilkan:
        flash(f"Tidak ditemukan konser dengan kata kunci '{query}'.", 'info')
    return render_template('konser.html', konser=hasil_pencarian_untuk_ditampilkan, search_active=True, search_query=query)

@app.route('/pembeli')
def kelola_pembeli():
    search_query = request.args.get('search_query', '').lower()
    sort_by = request.args.get('sort_by', 'nama_asc')
    semua_pembeli = Pembeli.query.all()
    
    if search_query:
        pembeli_hasil_filter = [pembeli for pembeli in semua_pembeli if search_query in pembeli.nama.lower() or search_query in pembeli.email.lower()]
    else:
        pembeli_hasil_filter = semua_pembeli
        
    pembeli_linked_list = LinkedList()
    for item_pembeli in pembeli_hasil_filter:
        pembeli_linked_list.append(item_pembeli)
    
    pembeli_untuk_diurutkan = pembeli_linked_list.to_list()
    
    if sort_by == 'nama_desc':
        pembeli_terurut = merge_sort(pembeli_untuk_diurutkan, key_untuk_sort=lambda p: p.nama, urutkan_terbalik=True)
    elif sort_by == 'id_asc':
        pembeli_terurut = merge_sort(pembeli_untuk_diurutkan, key_untuk_sort=lambda p: p.id)
    elif sort_by == 'id_desc':
        pembeli_terurut = merge_sort(pembeli_untuk_diurutkan, key_untuk_sort=lambda p: p.id, urutkan_terbalik=True)
    else: # nama_asc
        pembeli_terurut = merge_sort(pembeli_untuk_diurutkan, key_untuk_sort=lambda p: p.nama)
        
    return render_template('pembeli.html', pembeli=pembeli_terurut, search_query=search_query, sort_by=sort_by)

@app.route('/pembeli/tambah', methods=['POST'])
def tambah_pembeli():
    pembeli_baru = Pembeli(id=str(uuid.uuid4())[:8].upper(), nama=request.form['nama'], email=request.form['email'], telepon=request.form['telepon'])
    db.session.add(pembeli_baru)
    db.session.commit()
    flash('Pembeli berhasil ditambahkan!', 'success')
    return redirect(url_for('kelola_pembeli'))

@app.route('/pembeli/edit/<string:id_pembeli>', methods=['GET', 'POST'])
def edit_pembeli(id_pembeli):
    pembeli_yang_diedit = Pembeli.query.get_or_404(id_pembeli)
    if request.method == 'POST':
        pembeli_yang_diedit.nama = request.form['nama']
        pembeli_yang_diedit.email = request.form['email']
        pembeli_yang_diedit.telepon = request.form['telepon']
        db.session.commit()
        flash('Data pembeli berhasil diperbarui!', 'success')
        return redirect(url_for('kelola_pembeli'))
    return render_template('edit_pembeli.html', pembeli=pembeli_yang_diedit)

@app.route('/pembeli/hapus/<string:id_pembeli>', methods=['POST'])
def hapus_pembeli(id_pembeli):
    pembeli_yang_dihapus = Pembeli.query.get(id_pembeli)
    if pembeli_yang_dihapus:
        Transaksi.query.filter_by(id_pembeli=id_pembeli).update({"id_pembeli": None})
        db.session.delete(pembeli_yang_dihapus)
        db.session.commit()
        flash('Pembeli berhasil dihapus. Transaksi terkait dijadikan anonim.', 'success')
    else:
        flash('Pembeli tidak ditemukan!', 'error')
    return redirect(url_for('kelola_pembeli'))

@app.route('/transaksi')
def kelola_transaksi():
    search_query = request.args.get('search_query', '')
    query = Transaksi.query.options(joinedload(Transaksi.pembeli), joinedload(Transaksi.detail_tiket).joinedload(Tiket.konser))
    semua_transaksi = query.all()
    
    if search_query:
        search_term_lower = search_query.lower()
        transaksi_hasil_filter = [t for t in semua_transaksi if search_term_lower in t.id_transaksi.lower() or (t.nomor_tiket and search_term_lower in t.nomor_tiket.lower()) or (t.nama_konser and search_term_lower in t.nama_konser.lower()) or (t.pembeli and search_term_lower in t.pembeli.nama.lower())]
    else:
        transaksi_hasil_filter = semua_transaksi

    transaksi_linked_list = LinkedList()
    for item_transaksi in transaksi_hasil_filter:
        transaksi_linked_list.append(item_transaksi)
    transaksi_untuk_diurutkan = transaksi_linked_list.to_list()

    transaksi_terurut = merge_sort(transaksi_untuk_diurutkan, key_untuk_sort=lambda t: t.tanggal, urutkan_terbalik=True)

    tiket_tersedia = Tiket.query.filter_by(status='Tersedia').options(joinedload(Tiket.konser)).all()
    list_pembeli = Pembeli.query.all()
    
    return render_template('transaksi.html', transactions=transaksi_terurut, available_tickets=tiket_tersedia, pembeli_list=list_pembeli, search_query=search_query)

@app.route('/transaksi/tambah', methods=['POST'])
def tambah_transaksi():
    nomor_tiket = request.form['nomor_tiket']
    id_pembeli = request.form['id_pembeli']
    tiket_dibeli = Tiket.query.get(nomor_tiket)
    if not tiket_dibeli or tiket_dibeli.status != 'Tersedia':
        flash('Tiket tidak valid atau sudah terjual!', 'error')
    else:
        tiket_dibeli.status = 'Terjual'
        transaksi_baru = Transaksi(id_transaksi=str(uuid.uuid4())[:8].upper(), nomor_tiket=nomor_tiket, id_pembeli=id_pembeli, nama_konser=tiket_dibeli.konser.nama, tanggal=datetime.date.today(), harga_transaksi=tiket_dibeli.konser.harga)
        db.session.add(transaksi_baru)
        db.session.commit()
        flash('Transaksi berhasil ditambahkan!', 'success')
    return redirect(url_for('kelola_transaksi'))

@app.route('/transaksi/hapus/<string:id_transaksi>', methods=['POST'])
def hapus_transaksi(id_transaksi):
    transaksi_yang_dihapus = Transaksi.query.get(id_transaksi)
    if transaksi_yang_dihapus:
        if transaksi_yang_dihapus.detail_tiket:
            transaksi_yang_dihapus.detail_tiket.status = 'Tersedia'
        db.session.delete(transaksi_yang_dihapus)
        db.session.commit()
        flash('Transaksi berhasil dihapus dan status tiket dikembalikan.', 'success')
    else:
        flash('Transaksi tidak ditemukan!', 'error')
    return redirect(url_for('kelola_transaksi'))

# Titik masuk utama aplikasi
if __name__ == '__main__':
    # Pastikan folder upload ada
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    # Buat tabel database jika belum ada
    with app.app_context():
        db.create_all()
    # Jalankan aplikasi dalam mode debug
    app.run(debug=True)

