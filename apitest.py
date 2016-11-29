import requests, json

auth = {"apikey":"","username":"","userkey":""}
data = json.dumps(auth)
headers = {"Content-Type": "application/json"}
getToken = requests.post('https://api.thetvdb.com/login', data=data, headers=headers).json()
token = {"Authorization: Bearer " + (getToken['token'])}
