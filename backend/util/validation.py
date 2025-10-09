import requests
import json
import os 

params = {
  'models': 'nudity-2.1,weapon,alcohol,recreational_drug,medical,properties,type,quality,scam,text-content,gore-2.0,text,qr-content,tobacco,genai,violence,self-harm,gambling',
  'api_user': os.environ.get('SIGHTENGINE_API_USER'),
  'api_secret': os.environ.get('SIGHTENGINE_API_SECRET')
}
files = {'media': open('/full/path/to/image.jpg', 'rb')}
r = requests.post('https://api.sightengine.com/1.0/check.json', files=files, data=params)

output = json.loads(r.text)