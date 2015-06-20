import urllib2, urllib
import json
import sys
import os

token = os.environ["FREESOUND_TOKEN"]
word = str(sys.argv[1])
print word
url = "http://www.freesound.org/apiv2/search/text/?query="+word+"&token="+token+"&filter=duration:[*%20TO%204]"
response = urllib2.urlopen(url)
sounds = json.load(response)
for i in range(0,8):
	id = sounds['results'][i]['id']
	url = "http://www.freesound.org/apiv2/sounds/%s/?token=%s&" % (id,token)
	response = urllib2.urlopen(url)
	sound = json.load(response)
	file = sound['previews']['preview-lq-mp3']
	testfile = urllib.URLopener()
	testfile.retrieve(file,str(i)+".mp3")

