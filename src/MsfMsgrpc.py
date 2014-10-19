__author__ = 'dave'

import httplib

import msgpack


class MsfMsgrpc:
    def __init__(self, host, port, username, password):
        self.host = str(host)
        self.port = int(port)
        self.username = str(username)
        self.password = str(password)
        self.client = httplib.HTTPConnection(self.host, self.port)

    def send(self, params):
        headers = {"Content-type": "binary/message-pack"}
        self.client.request("POST", "/api", msgpack.packb(params), headers)
        response = self.client.getresponse()
        content = msgpack.unpackb(response.read())
        return content

    def login(self):
        return self.send(["auth.login", self.username, self.password])

    def moduleStats(self, token):
        return self.send(["core.module_stats", token])

    def createConsole(self, token):
        return self.send(["console.create", token])

    def destroyConsole(self, token, consoleId):
        return self.send(["console.destroy", token, consoleId])

    def consoleWrite(self, token, consoleId, data):
        return self.send(["console.write", token, consoleId, data])

    def consoleRead(self, token, consoleId):
        return self.send(["console.read", token, consoleId])
