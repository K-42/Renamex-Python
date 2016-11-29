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

#adding .json() to the end of getToken turns it into a dictionary, which makes it easier to separate the token part of the response. decodes?
#without this, the response item is a string: I couldn't get json.load/s to work on this for some reason.


