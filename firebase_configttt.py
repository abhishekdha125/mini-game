# firebase_config.py
import firebase_admin
from firebase_admin import credentials, db

def init_firebase():
    cred = credentials.Certificate("tik-tak-toe-37f7b-firebase-adminsdk-fbsvc-461d41dd71.json")  # path to your downloaded key
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://tik-tak-toe-37f7b-default-rtdb.asia-southeast1.firebasedatabase.app/'  # change this
    })
