import firebase_admin
import os, json

from firebase_admin import credentials, firestore

firebase_json = os.environ.get("FIREBASE_KEY_JSON")
cred = credentials.Certificate(json.loads(firebase_json))

firebase_admin.initialize_app(cred)

db = firestore.client()
