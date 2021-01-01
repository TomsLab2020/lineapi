import streamlit as st
import io
import requests
from PIL import Image, ImageDraw, ImageFont


st.title('顔認識アプリ')

subscription_key = 'c5017c1f184d4d71849be3597abbc8bf'
assert subscription_key

face_api_url = 'https://20201213mt.cognitiveservices.azure.com/face/v1.0/detect'

upload_file = st.file_uploader('Choose an image...', type = 'jpg')
if upload_file is not None:
    img = Image.open(upload_file)
    with io.BytesIO() as output:
        img.save(output, format='JPEG')
        binary_img = output.getvalue()
    headers = {
        'Content-Type':'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscription_key
    }
    params = {
        'returnFaceId': 'true',
        'returnfaceAttributes' : 'age, gender, smile, facialHair, headPose, glasses, emotion, hair, makeup, accessories, blur, exposure, noise'
    }
    res = requests.post(face_api_url, params=params, headers=headers, data=binary_img)

    results = res.json()
    for result in results:
        rect = result['faceRectangle']
        age = result['faceAttributes']['age']
        gender = result['faceAttributes']['gender']
        label = f'{gender} : {age}'
        
        draw = ImageDraw.Draw(img)
        draw.rectangle([(rect['left'], rect['top']), (rect['left'] + rect['height'], rect['top'] + rect['width'])],
                    fill=None, outline='green', width=5)
#        font = ImageFont.truetype("meiryob.ttc", size=60)
        draw.text((rect['left'], rect['top']-70), text = label, fill = 'white')
#        draw.text((rect['left'], rect['top']-70), text = label, font = font, fill = 'white')
        
    st.image(img, caption='Uploaded Image', use_column_width=True)



