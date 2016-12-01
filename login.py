import requests, json

def login():
    try:
        with open('local.auth') as f:
            auth = f.read()
        headers = {"Content-Type": "application/json"}
        getToken = requests.post('https://api.thetvdb.com/login', data=auth, headers=headers).json()
        token = {"Authorization: Bearer " + (getToken['token'])}
        print("Login successful.")
    except FileNotFoundError:
        print ("Login failed. API credentials for TVDB have not been set.")
