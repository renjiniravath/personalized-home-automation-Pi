import http.client
import json
from display import displayMessage

def makeAPIRequest(method, url):
    apiConn = http.client.HTTPConnection("192.168.0.191", 8080, timeout=10)
    apiConn.request(method, url)
    res = apiConn.getresponse()
    if res.status == 401:
        print("Unauthorized User")
        displayMessage("Unauthorized User")
        return {}
    elif res.status != 200:
        print("Unexpected error, please check server logs")
        displayMessage("Unexpected error")
        return {}
    data = res.read()
    apiConn.close()
    return json.loads(data)