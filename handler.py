import http.client
import json

def makeAPIRequest(method, url):
    apiConn = http.client.HTTPConnection("192.168.0.191", 8080, timeout=10)
    apiConn.request(method, url)
    res = apiConn.getresponse()
    data = res.read()
    apiConn.close()
    return json.loads(data)