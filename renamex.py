import configparser, json, os, re, requests

#user configuration
config = configparser.ConfigParser()
if os.path.exists('./renamexconfig.ini'):
  config.read('renamexconfig.ini')
else:
  from functions import makeConfig
  makeConfig()
  config.read('renamexconfig.ini')

files = ['Dexter- S01E09.1080p.5.1Ch.BluRay.ReEnc-DeeJayAhmed.mp4','Dexter- S01E11.1080p.5.1Ch.BluRay.ReEnc-DeeJayAhmed.mp4','Westworld S01e10.mp4','Dexter- S01E03.1080p.5.1Ch.BluRay.ReEnc-DeeJayAhmed.mp4','Breaking Bad 1x5 720p.BRrip.Sujaidr.mp4','The.Walking.Dead - 0704 - Web of Lies - .1080p.WEB-DL.x264-FUM[ettv].txt', 'extant - s1e3 .mp4' ]

#regex
handleCurrentName = re.compile(r'''
  ([a-z-_\.\s]*) 					#series name
  (s(\d{,2})e(\d{,2})|(\d{3,4})|(\d{1,2})x(\d{1,2})) 	#episode number (S01E01, 1x1, 101)
  (.*) 							#episode title (junk)
  (\.\w*$) 						#file extension
  ''',re.VERBOSE|re.I)

def fileNamer(x):
  currentName = handleCurrentName.search(files[x])
  sName = re.sub(r'[\W_]',' ', currentName.group(1)).title().strip(' ') #removes junk and trailing white space from series name
  sNum = currentName.group(2).strip('s,S')[:2].lstrip('0').strip('x,X,e,E')
  eNum = currentName.group(2)[-2:].lstrip('0').strip('x,X,e,E')
  eTitle= ""
  fileExt = currentName.group(9)
  try:
    with open ('renamex.seriesdata') as datafile:                
      localDB = json.load(datafile)
      datafile.close()
      if sName in localDB:
        for i in range (len(localDB[sName]['data'])): #loop through all episodes in series
          if ((localDB[sName]['data'][i]['airedSeason']) == int(sNum)and(localDB[sName]['data'][i]['airedEpisodeNumber']) == int(eNum)):
            eTitle=(localDB[sName]['data'][i]['episodeName'])
            break
          else:
            eTitle=""
      else:
        getSeriesData()
        with open ('renamex.seriesdata') as datafile:                
          localDB = json.load(datafile)
          datafile.close()
          if sName in localDB:
            for i in range (len(localDB[sName]['data'])): #loop through all episodes in series
              if ((localDB[sName]['data'][i]['airedSeason']) == int(sNum)and(localDB[sName]['data'][i]['airedEpisodeNumber']) == int(eNum)):
                eTitle=(localDB[sName]['data'][i]['episodeName'])
                break
              else:
                eTitle=""
  except FileNotFoundError:
            getSeriesData()
            with open ('renamex.seriesdata') as datafile:                
              localDB = json.load(datafile)
              datafile.close()
              if sName in localDB:
                for i in range (len(localDB[sName]['data'])): #loop through all episodes in series
                  if ((localDB[sName]['data'][i]['airedSeason']) == int(sNum)and(localDB[sName]['data'][i]['airedEpisodeNumber']) == int(eNum)):
                    eTitle=(localDB[sName]['data'][i]['episodeName'])
                    break
              else:
                eTitle=""
  return sName, sNum, eNum, eTitle, fileExt

def getSeriesData():
    currentName = handleCurrentName.search(files[x])
    sName = re.sub(r'[\W_]',' ', currentName.group(1)).title().strip(' ')
    if config['token']['token'] == "":
        if login() == "OK":
            print("No token details. Logged in: trying again.")
            getSeriesData()
        else:
            print("No token details. Tried to fetch but login failed. Check that renamexconfig.ini has correct authorisation data.")
    else:
        authHeader = {'Authorization': 'Bearer ' + (config['token']['token'])}
        payload = {'name': sName}
        get = requests.get('https://api.thetvdb.com/search/series', headers=authHeader, params = payload)
        response = get.json() #there might be multiple series here
        status = get.status_code
        if status == int(200):
            idData = response
            for i in range (len(idData['data'])): #so loop through IDs
                if ((idData['data'][i]['seriesName']) == sName): #to find the ID of the correct series
                    id = idData['data'][i]['id'] #store the ID
                    get = requests.get('https://api.thetvdb.com/series/'+str(id)+'/episodes', headers=authHeader) #and use it to get the correct data
                    response = get.json() 
                    status = get.status_code
                    if status == int(200):
                        try:
                            with open ('renamex.seriesdata') as datafile:                
                                localDB = json.load(datafile) #grab the local database
                                datafile.close()
                            with open ('renamex.seriesdata', 'w') as datafile:  
                                newData = {}
                                newData[sName]=response #adds series name as key to response value in "newData" dictionary
                                localDB.update(newData) #add the dictionary to the local database
                                json.dump(localDB,datafile) #save the local database
                                datafile.close()
                        except FileNotFoundError:
                            with open ('renamex.seriesdata', 'w') as datafile:
                                localDB={}
                                localDB[sName]=response
                                json.dump(localDB, datafile)
                                datafile.close()
                    else:
                        print("Uh oh! Something went wrong with the series ID. The server returned status code " + str(status) + ": " + str(response))
        else:
            print("Uh oh! Something went wrong when searching for the series name. The server returned status code " + str(status) + ": " + str(response))

class Opt():
  def __init__(self):
    namePieces = fileNamer(x)
    self.sName = namePieces[0]
    self.sNum = namePieces[1]
    self.eNum = namePieces[2]
    self.eTitle = namePieces[3]
    self.fileExt = namePieces[4]
  def opt1(self): #S01E01
    filename = ((self.sName) 
    + " - " 
    + ("S" if config['user']['caps'] == "y" else "s") 
    + (str(self.sNum) if int(self.sNum) >=10 else "0"+str(self.sNum)) 
    + ("E" if config['user']['caps'] == "y" else "e") 
    + (str(self.eNum) if int(self.eNum) >=10 else "0"+str(self.eNum)) 
    + (" - " if self.eTitle != "" else "")
    + self.eTitle
    + self.fileExt) 
    return filename
  def opt2(self): #S1E1
    filename = ((self.sName)
    + " - "
    + ("S" if config['user']['caps'] == "y" else "s")
    + str(self.sNum)
    + ("E" if config['user']['caps'] == "y" else "e")
    + str(self.eNum)
    + (" - " if self.eTitle != "" else "")
    + self.eTitle
    + self.fileExt) 
    return filename
  def opt3(self): #1x1
    filename = ((self.sName)
    + " - " 
    + str(self.sNum)
    + ("X" if config['user']['caps'] == "y" else "x") 
    + str(self.eNum) 
    + (" - " if self.eTitle != "" else "") 
    + self.eTitle
    + self.fileExt) 	
    return filename
  def opt4(self): #101
    filename = ((self.sName) 
    + " - " 
    + str(self.sNum) 
    + (str(self.eNum) if int(self.eNum) >=10 else "0"+str(self.eNum))
    + " - "
    + (" - " if self.eTitle != "" else "")
    + self.fileExt)
    return filename

#print files
x=0
for i in files:
  newFile = getattr(Opt(), config['user']['numberType'])()
  print (newFile)
  x+=1
