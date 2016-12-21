import re

files = ['Dexter- S01E10.1080p.5.1Ch.BluRay.ReEnc-DeeJayAhmed.mp4','Breaking Bad 1x13 720p.BRrip.Sujaidr.mp4','The.Walking.Dead - 1104 - Web of Lies - .1080p.WEB-DL.x264-FUM[ettv].txt', 'extant - s14e14 .mp4' ]

#regex
pull= re.compile(r'''
	([a-z-_\.\s]*) 						#series name
	(s(\d{,2})e(\d{,2})|(\d{3,4})|(\d{1,2})x(\d{1,2})) 	#episode number (S01E01, 1x1, 101)
	(.*) 							#episode title (junk)
	(\.\w*$) 						#file extension
    	''',re.VERBOSE|re.I)
	
caps = "y"
choice = "opt1"
eTitle = "Temporary"

def namer(x):
	oldName = pull.search(files[x])
	sName = re.sub(r'[\W_]',' ', oldName.group(1)).title().strip(' ') #removes junk and trailing white space from series name
	sNum = oldName.group(2).strip('s,S')[:2].lstrip('0').strip('x,X,e,E')
	eNum = oldName.group(2)[-2:].lstrip('0').strip('x,X,e,E')
	fileExt = oldName.group(9)
	return sName, sNum, eNum, fileExt

class opt():
	@staticmethod
 	def opt1(x): #S01E01
		sName = namer(x)[0]
		sNum = namer(x)[1]
		eNum = namer(x)[2]
		fileExt = namer(x)[3]
		filename = ((sName) 
		+ " - " 
		+ ("S" if caps == "y" else "s") 
		+ (str(sNum) if int(sNum) >=10 else "0"+str(sNum)) 
		+ ("E" if caps == "y" else "e") 
		+ (str(eNum) if int(eNum) >=10 else "0"+str(eNum)) 
		+ " - "
		+ eTitle
		+ fileExt) 
		return filename
	@staticmethod
	def opt2(x): #S1E1
		filename = ((sName)
		+ " - "
		+ ("S" if caps == "y" else "s")
		+ str(sSeason)
		+ ("E" if caps == "y" else "e")
		+ str(sEpisode)
		+ " - "
		+ eTitle)
		return filename
	@staticmethod
	def opt3(): #1x1
		filename = ((sName)
		+ " - " 
		+ str(sSeason)
		+ ("X" if caps == "y" else "x") 
		+ str(sEpisode) 
		+ " - " 
		+ eTitle)
		return filename
	@staticmethod
	def opt4(): #101
		filename = ((sName) 
		+ " - " 
		+ str(sSeason) 
		+ (str(sEpisode) if int(sEpisode) >=10 else "0"+str(sEpisode))
		+ " - "
		+ eTitle)
		return filename

#print files
x=0
for i in files:
	newFile = getattr(opt, choice)(x)
	print (newFile)
	x+=1
