import os
import psutil
import time
import json
from sentinel import Sentinel
from PIL import Image
import requests
from io import BytesIO


# your Auth key generated from app.sentinelengine.ai/authkeys
AUTH_KEY = os.getenv("SENTINEL_AUTH_KEY")
# your Device ID
DEVICE_ID = os.getenv("SENTINEL_DEVICE_ID")
# Enterprise accounts may use a custom domain to post their data
CUSTOM_DOMAIN = os.getenv("SENTINEL_DOMAIN") or "solo"

# Initialise a Sentinel API client
SentinelClient = Sentinel(AUTH_KEY, CUSTOM_DOMAIN)

# Grab a random image and convert it to bytes to upload to the file uploader
def get_image():
    imgurl = "https://www.fillmurray.com/200/300"
    img = Image.open(requests.get(imgurl, stream=True).raw)
    
    # Create a buffer to hold the bytes
    buf = BytesIO()
    img.save(buf, 'jpeg')
    buf.seek(0)

    # Read the bytes from the buffer
    image_bytes = buf.read()
    buf.close()
    return image_bytes

img = get_image()
response = SentinelClient.fileupload(DEVICE_ID, img, "test-image", "image/jpeg")
print("File uploaded to Sentinel Engine")
print(response.text)

