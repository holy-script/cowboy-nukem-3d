from appwrite.client import Client
from appwrite.services.functions import Functions
from secret import *
import json

client = Client()

(client
 .set_endpoint(API_ENDPOINT)
 .set_project(PROJECT_ID)
 .set_key(API_KEY)
 )

functions = Functions(client)

inputs = {
    'email': '',
    'pwd': '',
    'otp': '',
    'phone': '',
}


def ping():
    return functions.create_execution(PING_ID)


def signup():
    payload = json.dumps({
        'flow': 'signup',
        'data': inputs
    })
    return functions.create_execution(AUTH_ID, payload)


def login():
    payload = json.dumps({
        'flow': 'login',
        'data': inputs
    })
    return functions.create_execution(AUTH_ID, payload)


def otp():
    payload = json.dumps({
        'flow': 'verify',
        'data': inputs
    })
    return functions.create_execution(AUTH_ID, payload)
