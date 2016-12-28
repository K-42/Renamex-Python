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

class Opt():
        def __init__(self):
                self.sName = namer(x)[0]
                self.sNum = namer(x)[1]
                self.eNum = namer(x)[2]
                self.fileExt = namer(x)[3]
        def opt1(self): #S01E01
                filename = ((self.sName) 
                + " - " 
                + ("S" if caps == "y" else "s") 
                + (str(self.sNum) if int(self.sNum) >=10 else "0"+str(self.sNum)) 
                + ("E" if caps == "y" else "e") 
                + (str(self.eNum) if int(self.eNum) >=10 else "0"+str(self.eNum)) 
                + " - "
                + eTitle
                + self.fileExt) 
                return filename
        def opt2(self): #S1E1
                filename = ((self.sName)
                + " - "
                + ("S" if caps == "y" else "s")
                + str(self.sNum)
                + ("E" if caps == "y" else "e")
                + str(self.eNum)
                + " - "
                + eTitle
                + self.fileExt) 
                return filename
        def opt3(self): #1x1
                filename = ((self.sName)
                + " - " 
                + str(self.sNum)
                + ("X" if caps == "y" else "x") 
                + str(self.eNum) 
                + " - " 
                + eTitle
                + self.fileExt) 	
                return filename
        def opt4(self): #101
                filename = ((self.sName) 
                + " - " 
                + str(self.sNum) 
                + (str(self.eNum) if int(self.eNum) >=10 else "0"+str(self.eNum))
                + " - "
                + eTitle
                  + self.fileExt)
                return filename

#print files
x=0
for i in files:
        newFile = getattr(Opt(), choice)()
        print (newFile)
        x+=1
