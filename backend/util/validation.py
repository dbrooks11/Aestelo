import json

import requests
from flask import current_app


def photo_validation(*photos):

  params = {
    'workflow': current_app.config['SIGHTENGINE_WORKFLOW_ID'],
    'api_user': current_app.config['SIGHTENGINE_API_USER'],
    'api_secret': current_app.config['SIGHTENGINE_API_SECRET']
  }

  valid_photos =[]
  errors = []

  try:
    pht_count = 0
    for photo in photos:
      pht_count += 1
      files = {'media': ('photo.jpg', photo, 'photo/jpeg')}
      r = requests.post('https://api.sightengine.com/1.0/check-workflow.json', files=files, data=params)

      output = json.loads(r.text)

      if output['status'] == 'failure':
        errors.append({f'photo {pht_count} failed: {output['error']}'})
        continue

      if output['summary']['action'] == 'reject':
        errors.append(f'photo {pht_count} rejected: Summary - {output['summary']['reject_reason']},\n {output['summary']['reject_prob']}')
        continue
      
      valid_photos.append(photo)
  except requests.exceptions.Timeout:
    errors.append(f"photo {pht_count}: Moderation timeout - photo allowed")
    valid_photos.append(photo)

  except Exception as e:
    errors.append(f"photo {pht_count}: Error - {str(e)}")

  return valid_photos, errors