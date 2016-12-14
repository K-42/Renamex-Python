import requests, json

def login():
    try:
        with open('local.auth') as f:
            auth = f.read() #gets credentials from file as JSON string
            headers = {"Content-Type": "application/json"}
            post = requests.post('https://api.thetvdb.com/login', data=auth, headers=headers)
            response = post.json()
            status = post.status_code
            if status == int(200): 
                authHeader = {'Authorization': 'Bearer ' + response['token']} #if login successful, add token to required header format and dump to file for future calls
                with open('local.token', 'w') as f:
                    json.dump(authHeader, f)
                    print("Logged in!")
            else:
                print("Uh oh! Something went wrong. The server returned status code " + str(status) + ": " + str(response))
    except FileNotFoundError:
        print ("Error: TVDB credentials missing.")
    
def refresh():
    #todo: needs to check age of current token file. if >=24 hours, call login() instead.
    try:
        with open('local.token') as f:
            authHeader = json.load(f) #gets required header from file in dictionary format
            get = requests.get('https://api.thetvdb.com/refresh_token', headers=authHeader)
            response = get.json()
            status = get.status_code
            if status == int(200):
                authHeader = {'Authorization': 'Bearer ' + response['token']}
                with open('local.token', 'w') as f:
                    json.dump(authHeader, f)
                    print("Token refreshed!")
            else:
                print("Uh oh! Something went wrong. The server returned status code " + str(status) + ": " + str(response))
    except FileNotFoundError:
        print ("Couldn't find a token to refresh.")
