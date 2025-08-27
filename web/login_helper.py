import requests
import os

# Tu API Key de Firebase (desde Project Settings → Web API Key)
FIREBASE_API_KEY = 'TU_API_KEY_DE_FIREBASE'

def login(email, password):
    url = f'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}'
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    r = requests.post(url, json=payload)
    if r.status_code == 200:
        return r.json()  # login correcto
    else:
        return None     # login fallido
