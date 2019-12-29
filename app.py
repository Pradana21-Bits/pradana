from flask import Flask, render_template, redirect, \
    url_for, request, get_flashed_messages, flash, session
from mysql import connector

app = Flask(__name__)

# Kunci rahasia
app.config['SECRET_KEY'] = 'wkwkwkwkwkwkwkwkw'


# Koneksi ke database
db = connector.connect(
    host        = "localhost",
    user        = "root",
    passwd      = "",
    database    = "panpin"
)

if db.is_connected():
    print('=========Connected==========')

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='dashboard')

@app.route('/login', methods=['POST', 'GET'])
def login():
    # Jika user submit data dari form
    if request.method == 'POST':

        # Mengambil data dari form
        nim = request.form['nim']
        password = request.form['password']

        # Untuk menjalankan perintah SQL
        cur = db.cursor()
        cur.execute('select * from mahasiswa where nim=%s', (nim,))
        user = cur.fetchone()
        cur.close()

        # Jika usernya ada, maka:
        if user:

            # Jika password dari form sama dengan password di database user,
            if password == user[3]:

                # Maka login
                session['nama'] = user[1]
                session['nim'] = user[0]

                # Membuat tulisan menyapa user
                flash(f'Selamat datang {user[1]}', 'success')

                # Jika berhasil login, maka dialihkan ke halaman home.
                return redirect(url_for('dashboard'))

            else:
                flash('Password atau username salah')

    # Jika request == 'GET',
    return render_template('login.html', title='Login')


@app.route('/dashboard') #Jika home dipanggil di url
# Fungsi home dijalankan
def dashboard():
    nama = session['nama']
    cur = db.cursor()
    cur.execute('SELECT mahasiswa.nim, mahasiswa.nama, account.balance, peminjaman.jumlah_pinjaman, peminjaman.tanggal_pinjam, peminjaman.tanggal_pembayaran \
        FROM mahasiswa JOIN account\
        ON mahasiswa.account_id = account.id_account\
        JOIN peminjaman\
        ON mahasiswa.nim = peminjaman.nim_mahasiswa\
        where nama = %s ', (nama,))
    user = cur.fetchone()
    cur.close()
    return render_template('dashboard.html', title='dashboard', user=user)

@app.route('/team')
def about():
    return render_template('team.html', title='about')

@app.route('/kontak')
def kontak():
    return render_template('kontak.html', title='kontak')

@app.route('/logout')
def logout():

    # Untuk melogout user
    session.clear()

    # Munculkan pesan
    flash('Anda telah logout', 'danger')

    # Kembali ke home
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)