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
                    return "OK"
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

sName="Firefly"

def getSeriesData():
    try:
        with open('local.token') as f:
            authHeader = json.load(f)
            payload = {'name': sName}
            get = requests.get('https://api.thetvdb.com/search/series', headers=authHeader, params = payload)
            response = get.json() #there might be multiple series here
            status = get.status_code
            if status == int(200):
                idData = response
                for i in range (len(idData['data'])): #so loop through IDs
                    if ((idData['data'][i]['seriesName']) == sName): #to find the ID of the correct series
                        id = idData['data'][i]['id'] #store the ID
                        get = requests.get('https://api.thetvdb.com/series/'+str(id)+'/episodes', headers=authHeader) #and use it to get a new response object that is only the correct series
                        response = get.json() 
                        status = get.status_code
                        if status == int(200):
                            try:
                                with open ('local.data') as f:                
                                    localDB = json.load(f) #grab the local database
                                with open ('local.data', 'w') as f:  
                                    newData = {}
                                    newData[sName]=response #adds series name as key to response value in "newData" dictionary
                                    localDB.update(newData) #add the dictionary to the local database
                                    json.dump(localDB,f) #save the local database
                            except FileNotFoundError:
                                with open ('local.data', 'w') as f:
                                    localDB={}
                                    localDB[sName]=response
                                    json.dump(localDB, f)
                        else:
                            print("Uh oh! Something went wrong with the series ID. The server returned status code " + str(status) + ": " + str(response))
            else:
                print("Uh oh! Something went wrong when searching for the series name. The server returned status code " + str(status) + ": " + str(response))
    except FileNotFoundError:
        if login() == "OK":
            print("No token details. Logged in: trying again.")
            getSeriesData()
        else:
            print("No token details, Login failed. Check that local.auth has been configured.")
