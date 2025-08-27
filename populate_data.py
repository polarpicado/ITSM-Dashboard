import pyodbc
from faker import Faker
import firebase_admin
from firebase_admin import credentials, auth
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

# ---- GENERAR DATOS ----
fake = Faker()

departments = ['IT', 'HR', 'Finance', 'Marketing']
priorities = ['Low', 'Medium', 'High', 'Critical']
statuses = ['Open', 'In Progress', 'Resolved', 'Closed']
change_types = ['Standard', 'Emergency', 'Normal']
impacts = ['Low', 'Medium', 'High']

# ---- Usuarios ----
users = []
for _ in range(10):
    name = fake.name()
    dept = choice(departments)
    email = fake.email()
    password = 'Test1234'
    users.append((name, dept))
    
    # Crear usuario en Firebase
    auth.create_user(email=email, password=password, display_name=name)

cursor.executemany("INSERT INTO Users (UserName, Department) VALUES (?, ?)", users)
conn.commit()

# ---- Servicios ----
services = [('Email', 4), ('VPN', 2), ('CRM', 8), ('ERP', 24)]
cursor.executemany("INSERT INTO Services (ServiceName, SLA_Hours) VALUES (?, ?)", services)
conn.commit()

# ---- Incidentes ----
cursor.execute("SELECT UserID FROM Users")
user_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT ServiceID FROM Services")
service_ids = [row[0] for row in cursor.fetchall()]

incidents = []
for _ in range(20):
    start = fake.date_time_this_year()
    end = start + timedelta(hours=randint(1, 48))
    incidents.append((
        choice(user_ids),
        choice(service_ids),
        choice(priorities),
        choice(statuses),
        start,
        end
    ))

cursor.executemany("""
INSERT INTO Incidents (UserID, ServiceID, Priority, Status, StartDate, EndDate)
VALUES (?, ?, ?, ?, ?, ?)
""", incidents)
conn.commit()

# ---- Cambios ----
changes = []
for _ in range(10):
    req_date = fake.date_time_this_year()
    comp_date = req_date + timedelta(hours=randint(1, 72))
    changes.append((
        choice(service_ids),
        choice(change_types),
        choice(impacts),
        choice(statuses),
        req_date,
        comp_date
    ))

cursor.executemany("""
INSERT INTO Changes (ServiceID, ChangeType, Impact, Status, RequestDate, CompletionDate)
VALUES (?, ?, ?, ?, ?, ?)
""", changes)
conn.commit()

print("Datos de prueba insertados en SQL Server y usuarios creados en Firebase.")
conn.close()
