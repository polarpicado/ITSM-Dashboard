import pyodbc
from faker import Faker
import firebase_admin
from firebase_admin import credentials, auth, firestore
from random import choice, randint
from datetime import datetime, timedelta

# ---- CONFIGURACIÓN SQL SERVER ----
SERVER = '127.0.0.1,1433'
DATABASE = 'ITSM_Dashboard'
USERNAME = 'sa'
PASSWORD = 'SuperClave!234'

conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# ---- CONFIGURACIÓN FIREBASE ----
cred = credentials.Certificate("serviceAccountKey.json")  # tu archivo descargado
firebase_admin.initialize_app(cred)
db = firestore.client()

# ---- GENERAR DATOS ----
fake = Faker()

departments = ['IT', 'HR', 'Finance', 'Marketing']
priorities = ['Low', 'Medium', 'High', 'Critical']
statuses = ['Open', 'In Progress', 'Resolved', 'Closed']
change_types = ['Standard', 'Emergency', 'Normal']
impacts = ['Low', 'Medium', 'High']

# ---- USUARIOS ----
users = []
for _ in range(10):
    name = fake.name()
    dept = choice(departments)
    email = fake.email()
    password = 'Test1234'
    users.append((name, dept))

    # Crear usuario en Firebase Authentication
    auth.create_user(email=email, password=password, display_name=name)

# Insertar usuarios en SQL Server
cursor.executemany("INSERT INTO Users (UserName, Department) VALUES (?, ?)", users)
conn.commit()

# Insertar usuarios en Firestore con IDs consistentes
for idx, user in enumerate(users, start=1):
    db.collection('Users').document(str(idx)).set({
        'UserID': idx,
        'UserName': user[0],
        'Department': user[1]
    })

# ---- SERVICIOS ----
services = [('Email', 4), ('VPN', 2), ('CRM', 8), ('ERP', 24)]
cursor.executemany("INSERT INTO Services (ServiceName, SLA_Hours) VALUES (?, ?)", services)
conn.commit()

# Recuperar IDs
cursor.execute("SELECT UserID FROM Users")
user_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT ServiceID FROM Services")
service_ids = [row[0] for row in cursor.fetchall()]

# Insertar servicios en Firestore con IDs consistentes
for idx, service in enumerate(services, start=1):
    db.collection('Services').document(str(idx)).set({
        'ServiceID': idx,
        'ServiceName': service[0],
        'SLA_Hours': service[1]
    })

# ---- INCIDENTES ----
incidents = []
for _ in range(20):
    start = fake.date_time_this_year()
    end = start + timedelta(hours=randint(1, 48))
    incident = (
        choice(user_ids),
        choice(service_ids),
        choice(priorities),
        choice(statuses),
        start,
        end
    )
    incidents.append(incident)

# Insertar incidentes en SQL Server
cursor.executemany("""
INSERT INTO Incidents (UserID, ServiceID, Priority, Status, StartDate, EndDate)
VALUES (?, ?, ?, ?, ?, ?)
""", incidents)
conn.commit()

# Insertar incidentes en Firestore con IDs consistentes
for idx, incident in enumerate(incidents, start=1):
    db.collection('Incidents').document(str(idx)).set({
        'IncidentID': idx,
        'UserID': incident[0],
        'ServiceID': incident[1],
        'Priority': incident[2],
        'Status': incident[3],
        'StartDate': incident[4].isoformat(),
        'EndDate': incident[5].isoformat()
    })

# ---- CAMBIOS ----
changes = []
for _ in range(10):
    req_date = fake.date_time_this_year()
    comp_date = req_date + timedelta(hours=randint(1, 72))
    change = (
        choice(service_ids),
        choice(change_types),
        choice(impacts),
        choice(statuses),
        req_date,
        comp_date
    )
    changes.append(change)

# Insertar cambios en SQL Server
cursor.executemany("""
INSERT INTO Changes (ServiceID, ChangeType, Impact, Status, RequestDate, CompletionDate)
VALUES (?, ?, ?, ?, ?, ?)
""", changes)
conn.commit()

# Insertar cambios en Firestore con IDs consistentes
for idx, change in enumerate(changes, start=1):
    db.collection('Changes').document(str(idx)).set({
        'ChangeID': idx,
        'ServiceID': change[0],
        'ChangeType': change[1],
        'Impact': change[2],
        'Status': change[3],
        'RequestDate': change[4].isoformat(),
        'CompletionDate': change[5].isoformat()
    })

print("Datos de prueba insertados en SQL Server y Firestore, usuarios creados en Firebase.")
conn.close()
