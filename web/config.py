import pyodbc
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
import os

load_dotenv()

# SQL Server
SERVER = os.getenv("SQL_SERVER")
DATABASE = os.getenv("SQL_DATABASE")
USERNAME = os.getenv("SQL_USER")
PASSWORD = os.getenv("SQL_PASSWORD")

conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Firebase
cred = credentials.Certificate(os.getenv("FIREBASE_JSON"))
firebase_admin.initialize_app(cred)
db = firestore.client()
FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")
