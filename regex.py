import re

files = ['Dexter- s01E01.1080p.5.1Ch.BluRay.ReEnc-DeeJayAhmed.mp4','Breaking Bad 1x01 720p.BRrip.Sujaidr.mp4','The.Walking.Dead - 101 - Web of Lies - .1080p.WEB-DL.x264-FUM[ettv].txt']

pull= re.compile(r'''
	([a-z-_\.\s]*) 							#series name
	(s\d{,2}e\d{,2}|\d{3,4}|\dx\d{1,2}) 	#episode number (S01E01, 101, 1X01)
	(.*) 									#episode title (junk)
	(\.\w*$) 								#file extension
    ''',re.VERBOSE|re.I)
	
j=0
for i in files:
  oldName = pull.search(files[j])
  seriesTitle = re.sub(r'[\W_]',' ', oldName.group(1)).title()
  #if episode title = yes, then get title before manage white space, else:
  manageWhitespace = re.sub(r'\s+',' ', seriesTitle)
  newName = manageWhitespace + "- " + oldName.group(2).upper() + oldName.group(4)
  print(newName)
  j+=1