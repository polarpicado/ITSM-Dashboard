import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd

# ---- FIREBASE ----
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# ---- Exportar Incidents ----
incidents_docs = db.collection('Incidents').stream()
incidents_data = []

for doc in incidents_docs:
    d = doc.to_dict()
    incidents_data.append({
        "IncidentID": d.get("IncidentID"),
        "UserID": d.get("UserID"),
        "ServiceID": d.get("ServiceID"),
        "Priority": d.get("Priority"),
        "Status": d.get("Status"),
        "StartDate": d.get("StartDate"),
        "EndDate": d.get("EndDate")
    })

df_incidents = pd.DataFrame(incidents_data)
df_incidents.to_csv("Incidents.csv", index=False)
print("CSV de Incidents creado.")

# ---- Exportar Changes ----
changes_docs = db.collection('Changes').stream()
changes_data = []

for doc in changes_docs:
    d = doc.to_dict()
    changes_data.append({
        "ChangeID": d.get("ChangeID"),
        "ServiceID": d.get("ServiceID"),
        "ChangeType": d.get("ChangeType"),
        "Impact": d.get("Impact"),
        "Status": d.get("Status"),
        "RequestDate": d.get("RequestDate"),
        "CompletionDate": d.get("CompletionDate")
    })

df_changes = pd.DataFrame(changes_data)
df_changes.to_csv("Changes.csv", index=False)
print("CSV de Changes creado.")
