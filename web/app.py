from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import cursor, conn, db
import datetime
import requests
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"  # puedes poner algo más seguro

# ---------------------------
# Configuración de Firebase REST
# ---------------------------
FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")  # Añade esto en tu .env

def firebase_login(email, password):
    url = f'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}'
    payload = {"email": email, "password": password, "returnSecureToken": True}
    r = requests.post(url, json=payload)
    if r.status_code == 200:
        return r.json()  # login correcto
    else:
        return None  # login fallido

# ---- Rutas ----
@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login_route'))
    
    cursor.execute("""
        SELECT i.IncidentID, u.UserName, s.ServiceName, i.Priority, i.Status, i.StartDate, i.EndDate
        FROM Incidents i
        JOIN Users u ON i.UserID = u.UserID
        JOIN Services s ON i.ServiceID = s.ServiceID
    """)
    incidents = cursor.fetchall()
    return render_template('index.html', incidents=incidents)

@app.route('/login', methods=['GET', 'POST'], endpoint='login')
def login_route():  # renombrado para evitar conflicto
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Endpoint REST para login en Firebase
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }

        r = requests.post(url, json=payload)
        if r.status_code == 200:
            # Login correcto: guardamos en sesión, pero sin flash
            session['user'] = email
            return redirect(url_for('index'))
        else:
            # Login fallido: mostramos mensaje de error
            flash("Usuario o contraseña incorrectos", "danger")

    return render_template('login.html')


@app.route('/new', methods=['GET', 'POST'])
def new_incident():
    if request.method == 'POST':
        user_id = request.form['user_id']
        service_id = request.form['service_id']
        priority = request.form['priority']
        status = request.form['status']
        start_date = datetime.datetime.now()
        end_date = start_date + datetime.timedelta(hours=24)

        cursor.execute("""
            INSERT INTO Incidents (UserID, ServiceID, Priority, Status, StartDate, EndDate)
            VALUES (?, ?, ?, ?, ?, ?)
        """, user_id, service_id, priority, status, start_date, end_date)
        conn.commit()
        return redirect(url_for('index'))

    cursor.execute("SELECT UserID, UserName FROM Users")
    users = cursor.fetchall()
    cursor.execute("SELECT ServiceID, ServiceName FROM Services")
    services = cursor.fetchall()
    return render_template('incident_form.html', users=users, services=services)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
