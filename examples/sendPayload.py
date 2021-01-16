import os
import psutil
import time
import json 
from sentinel import Sentinel

# your Auth key generated from app.sentinelengine.ai/authkeys
AUTH_KEY = os.getenv("SENTINEL_AUTH_KEY")
# your Device ID
DEVICE_ID = os.getenv("SENTINEL_DEVICE_ID")
# Enterprise accounts may use a custom domain to post their data
CUSTOM_DOMAIN = os.getenv("SENTINEL_DOMAIN") or "solo"

# Initialise a Sentinel API client
SentinelClient = Sentinel(AUTH_KEY, CUSTOM_DOMAIN)

# A simple check for the psutil values
def check_exists(prop, attr=False):
   print(prop)
   if prop is None:
      return "N/A"
   else:
      return getattr(prop, attr) if isinstance(attr, str) else prop

# Gather some simple system metrics to post in the payload body
# note - some psustil methods won't work on different systems so check the docs and remove the ones thay don't work
def gathersysinfo():
   try: 
      sysInfo = {
         "cpuFrequency": check_exists(psutil.cpu_freq(), "current"),
         "usedSwapMemoryPercent": check_exists(psutil.swap_memory(), "percent"),
         "usedVMMEMPercent": check_exists(psutil.virtual_memory(), "percent"),
         "batteryPercent": check_exists(psutil.sensors_battery(), "percent"),
         "pluggedIn": check_exists(psutil.sensors_battery(), "power_plugged"),
         "temperatureSensors": check_exists(psutil.sensors_temperatures())
      }

      return sysInfo
   except Exception as e:
      raise Exception("Error getting a system value - some psutil methods won't work on all systems, remove the erroneous value:", e)

# create a valid payload from the gathered data.
# Data must e sent with a deviceId and payload containing yor custom data
def generate_sentinel_payload(data):
   payload = {
      "deviceId": DEVICE_ID,
      "payload": data
   }
   print(payload)
   jsonPayload = json.dumps(payload)

   return jsonPayload

while True:
  info = gathersysinfo()
  payload = generate_sentinel_payload(info)
  response = SentinelClient.sendpayload(payload)
  print(response.text);
  time.sleep(5)

