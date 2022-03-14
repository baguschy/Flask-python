from flask import Flask, render_template, request, make_response, url_for, redirect, session, flash, abort
from markupsafe import escape


app = Flask(__name__)
app.secret_key = 'MX5kpEAPPlGW4QaUUHb8'

# url statis dengan view html
@app.route('/')
def index():
    return render_template('index.html')

# url dinamis
@app.route('/profile/<name>')
def profile(name):
    return render_template('profile.html', user=name)


# url login 
@app.route('/login', methods=['GET', 'POST'])
def viewLogin():
    if request.method == 'POST':
        # membuat cookie
        respon = make_response('kamu sudah login, email kamu adalah ' + request.form['email'])
        respon.set_cookie('email', request.form['email'])

        # memuat halaman error
        if request.form['password'] == '':
            abort(401)

        # membuat session
        session['email'] = request.form['email']
        flash('kamu berhasil login!', 'success')
        return redirect(url_for('showDashboard'))

    # validasi session
    if 'email' in session:
        return redirect(url_for('showDashboard'))

    return render_template('login.html')

# error hendler
@app.errorhandler(401)
def page_not_found(e):
    return render_template('error_login.html'), 401

# url logout
@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

# url get cookie
@app.route('/getCookie')
def getCookie():
    emailUser = request.cookies.get('email')
    return 'email yang tersimpan di cookie adalah '+emailUser

# url akses get parameter
@app.route('/data')
def showData():
    cariNama = request.args.get('cariNama')
    sortData = request.args.get('sortData')
    if not cariNama:
        return 'Halaman Data'

    return 'hasil pencarian adalah '+cariNama+' dan urutkan data dari '+sortData

# if else di jinja
@app.route('/mahasiswa')
def showDataMahasiswa():
    cari = request.args.get('cari')
    return render_template('data.html', nama=cari)

# url for 
@app.route('/dashboard')
def showDashboard():
    return render_template('dashboard.html')