
from urllib import request
from urllib import parse

import urllib.request
import time
import hashlib

print ("python demo starting...")

url = "https://openapi.danmi.com/distributor/sendSMS"
accountSid="ef34dd71938a676af6472af070eb2769"
to="13981980452"
templateid="3284"
param="1234"
auth_token="d648c108fccce4f348d67e2279364299"

t = time.time()
timestamp = str((int(round(t * 1000))))
sig=accountSid+auth_token+timestamp
m1 = hashlib.md5()
m1.update(sig.encode("utf-8"))
sig = m1.hexdigest()	

data="accountSid="+accountSid+"&to="+to+"&templateid="+templateid+"&param="+param+"&timestamp="+timestamp+"&sig="+sig
headers = {   
    'Content-Type':'application/x-www-form-urlencoded',
    'User-Agent':'Mozilla/5.0 (Linux Android 6.0 Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36'
}
data=str.encode(data)

print("data sent to SMS server is:")
print(data)
req = request.Request(url, headers=headers, data=data)  #POST方法
page = request.urlopen(req).read()
page = page.decode('utf-8')
print("response from SMS server is:")
print(page)

print ("python demo finished")

