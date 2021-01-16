import os
import requests
from datetime import datetime

class Sentinel:
  def __init__(self, authKey, domain):
    self.authkey = authKey
    self.customdomain = domain
    self.baseurl = f'https://http-decoder.{self.customdomain}.sentinelengine.ai'

  def sendpayload(self, payload):
    headers = {
      'Authorization': self.authkey,
      'Content-Type': 'application/json'
    }
    return requests.request("POST", self.baseurl, headers=headers, data=payload)
  
  def fileupload(self, deviceId, file, filename, mimeType):
    headers = {
      'Authorization': self.authkey,
      'DeviceId': deviceId
    }

    files = {f'{filename}-{datetime.utcnow()}': (filename, file, mimeType)}

    uploadUrl = f'{self.baseurl}/upload'
    return requests.request("POST", uploadUrl, headers=headers, data={}, files=files)