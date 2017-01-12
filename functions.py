def makeConfig():
    config['auth'] =    {'username': '',
                          'apikey': '',
                          'userkey': ''}
    config['token'] =   {'token':''}
    config['user'] =    {'caps':'y',            #as default
                         'numbering':'opt1'}    #as default     
    with open ('renamexconfig.ini','w') as configFile:
        config.write(configFile)
        configfile.close()
        print("WARNING: No configuration file found. To enable API features, add your credentials to: " + os.getcwd() +"\\renamexconfig.ini.")

def login():
    auth = json.dumps(dict(config.items('auth')))
    headers = {"Content-Type": "application/json"}
    post = requests.post('https://api.thetvdb.com/login', data=auth, headers=headers)
    response = post.json()
    status = post.status_code
    if status == int(200): 
        config['token']['token'] = response ['token'] #if login successful, add token to config
        with open('renamexconfig.ini', 'w') as configfile:
            config.write(configfile)
            configfile.close()
            print("Logged in!")
            return "OK"
    else:
        print("Uh oh! Something went wrong. The server returned status code " + str(status) + ": " + str(response))
 
def refresh():
    authHeader = {'Authorization': 'Bearer ' + (config['token']['token'])}
    get = requests.get('https://api.thetvdb.com/refresh_token', headers=authHeader)
    response = get.json()
    status = get.status_code
    if status == int(200):
        config['token']['token'] = response ['token']
        with open('renamexconfig.ini', 'w') as configfile:
            config.write(configfile)
            configfile.close()
            print("Token refreshed!")
    else:
        print("Uh oh! Something went wrong. The server returned status code " + str(status) + ": " + str(response))

