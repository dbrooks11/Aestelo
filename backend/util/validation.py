import requests
import json
import os 

def image_validation(*images):

  params = {
    'models': os.environ.get('WORKFLOW_ID'),
    'api_user': os.environ.get('SIGHTENGINE_API_USER'),
    'api_secret': os.environ.get('SIGHTENGINE_API_SECRET')
  }

  valid_images =[]
  errors = []

  try:
    img_count = 0
    for image in images:
      img_count += 1

      files = {'media': ('image.jpg', image, 'image/jpeg')}
      r = requests.post('https://api.sightengine.com/1.0/check-workflow.json', files=files, data=params)

      output = json.loads(r.text)

      if output['status'] == 'failure':
        errors.append({f'Image {img_count} failed: {output['error']}'})
        continue

      if output['summary']['action'] == 'reject':
        errors.append(f'Image {img_count} rejected: Summary - {output['summary']['reject_reason']},\n {output['summary']['reject_prob']}')
        continue
      
      valid_images.append(image)
  except requests.exceptions.Timeout:
    errors.append(f"Image {img_count}: Moderation timeout - image allowed")
    valid_images.append(image)

  except Exception as e:
    errors.append(f"Image {img_count}: Error - {str(e)}")


  return valid_images, errors