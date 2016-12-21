import re

files = ['Dexter- S01E10.1080p.5.1Ch.BluRay.ReEnc-DeeJayAhmed.mp4','Breaking Bad 1x13 720p.BRrip.Sujaidr.mp4','The.Walking.Dead - 1104 - Web of Lies - .1080p.WEB-DL.x264-FUM[ettv].txt', 'extant - s14e14 .mp4' ]

#regex
pull= re.compile(r'''
	([a-z-_\.\s]*) 						#series name
	(s(\d{,2})e(\d{,2})|(\d{3,4})|(\d{1,2})x(\d{1,2}))	#episode number (S01E01, 1x1, 101)
	(.*) 							#episode title (junk)
	(\.\w*$) 						#file extension
        ''',re.VERBOSE|re.I)

#main processing loop
j=0
for i in files:
        oldName = pull.search(files[j])
        sName = re.sub(r'[\W_]',' ', oldName.group(1)).title().strip(' ') #removes junk and trailing white space from series name
        sSeason = oldName.group(2).strip('s,S')[:2].lstrip('0').strip('x,X,e,E')
        sEpisode= oldName.group(2)[-2:].lstrip('0').strip('x,X,e,E')
        #filenames
        #print((sSeason) +','+(sEpisode))
        #print((sName) +	" - S" + (sSeason if int(sSeason) >=10 else "0"+str(sSeason)) + "E" + (sEpisode if int(sEpisode) >=10 else "0"+str(sEpisode))) #if 0s +title
        #print((sName) + " - S" + (sSeason) + "E" + (sEpisode)) #if not 0s +title
        #print((sName) + " - " + (sSeason) + "x" + (sEpisode)) #if 1x1 +title
        #print((sName) + " - " + (sSeason) + (sEpisode if int(sEpisode) >=10 else "0"+str(sEpisode))) #if 101 +title
        j+=1
