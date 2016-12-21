import re

files = ['Dexter- S01E10.1080p.5.1Ch.BluRay.ReEnc-DeeJayAhmed.mp4','Breaking Bad 1x13 720p.BRrip.Sujaidr.mp4','The.Walking.Dead - 1104 - Web of Lies - .1080p.WEB-DL.x264-FUM[ettv].txt', 'extant - s14e14 .mp4' ]

#regex
pull= re.compile(r'''
	([a-z-_\.\s]*) 						#series name
	(s(\d{,2})e(\d{,2})|(\d{3,4})|(\d{1,2})x(\d{1,2}))      #episode number (S01E01, 1x1, 101)
	(.*) 							#episode title (junk)
	(\.\w*$) 						#file extension
        ''',re.VERBOSE|re.I)

caps = "y"
opt = 1
eTitle = "Temporary"

def opt1(): #S01E01
	filename = ((sName) 
	+ " - " 
	+ ("S" if caps == "y" else "s") 
	+ (str(sSeason) if int(sSeason) >=10 else "0"+str(sSeason)) 
	+ ("E" if caps == "y" else "e") 
	+ (str(sEpisode) if int(sEpisode) >=10 else "0"+str(sEpisode)) 
	+ " - " 
	+ eTitle)
	return filename
  
def opt2(): #S1E1
	filename = ((sName)
	+ " - "
	+ ("S" if caps == "y" else "s")
	+ str(sSeason)
	+ ("E" if caps == "y" else "e")
	+ str(sEpisode)
	+ " - "
	+ eTitle)
	return filename
  
def opt3(): #1x1
	filename = ((sName)
	+ " - " 
	+ str(sSeason)
	+ ("X" if caps == "y" else "x") 
	+ str(sEpisode) 
	+ " - " 
	+ eTitle)
	return filename
  	
def opt4(): #101
	filename = ((sName) 
	+ " - " 
	+ str(sSeason) 
	+ (str(sEpisode) if int(sEpisode) >=10 else "0"+str(sEpisode))
	+ " - "
	+ eTitle)
	return filename

#main processing loop
j=0
for i in files:
	oldName = pull.search(files[j])
	sName = re.sub(r'[\W_]',' ', oldName.group(1)).title().strip(' ') #removes junk and trailing white space from series name
	sSeason = oldName.group(2).strip('s,S')[:2].lstrip('0').strip('x,X,e,E')
	sEpisode= oldName.group(2)[-2:].lstrip('0').strip('x,X,e,E')
	if opt == 1:
                file = opt1()
		print (file)
		j+=1
