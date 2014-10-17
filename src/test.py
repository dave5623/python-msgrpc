__author__ = 'dave'

import msgpack
import httplib

host = "127.0.0.1"
port = 55552
username = "msf"
password = "6jyU0ff8"
client = httplib.HTTPConnection(host, port)
token = ""

def send(params):
    headers = {"Content-type" : "binary/message-pack"}
    client.request("POST", "/api", msgpack.packb(params), headers)
    response = client.getresponse()
    content = msgpack.unpackb(response.read())
    return content

def login():
    return send(["auth.login", username, password])

def moduleStats():
    return send(["core.module_stats", token])

def createConsole():
    return send(["console.create", token])

def destroyConsole(consoleId):
    return send(["console.destroy", token, consoleId])

def consoleWrite(consoleId, data):
    return send(["console.write", token, consoleId, data])

def consoleRead(consoleId):
    return send(["console.read", token, consoleId])


token = ""

token = login ()['token']

print "Token: " + token

stats = moduleStats ()
print "Module Stats: " + str(stats)

response = createConsole()
consoleId = response["id"]

print "Create Console: " + str(response)

response = consoleRead (consoleId)
print "Console Read: " + str(response)

response = consoleWrite (consoleId, "hosts")
print "Console Write: " + str(response)

response = consoleRead (consoleId)
print "Console Read: " + str(response)

response = destroyConsole(consoleId)
print "Destroy Console: " + str(response)