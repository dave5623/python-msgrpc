__author__ = 'dave'

import httplib
import msgpack

class msgrpc:
    def __init__(self, host, port, username, password):
        self.host = str(host)
        self.port = int(55552)
        self.username = str(username)
        self.password = str(password)
        self.client
        self.token

    def connect(self):
        self.client = httplib.HTTPConnection(self.host, self.port)
        self.token = ""

    def send(self, params):
        headers = {"Content-type" : "binary/message-pack"}
        self.client.request("POST", "/api", msgpack.packb(params), headers)
        response = self.client.getresponse()
        content = msgpack.unpackb(response.read())
        return content

    def login(self):
        return self.send(["auth.login", self.username, self.password])

    def moduleStats(self):
        return self.send(["core.module_stats", self.token])

    def createConsole(self):
        return self.send(["console.create", self.token])

    def destroyConsole(self, consoleId):
        return self.send(["console.destroy", self.token, consoleId])

    def consoleWrite(self, consoleId, data):
        return self.send(["console.write", self.token, consoleId, data])

    def consoleRead(self, consoleId):
        return self.send(["console.read", self.token, consoleId])
