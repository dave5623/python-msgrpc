__author__ = 'dave'

import msgrpc

host = "127.0.0.1"
port = 55552
username = "msf"
password = "6jyU0ff8"

msf_msgrpc = msgrpc(host, port, username, password)

token = msf_msgrpc.login ()['token']

print "Token: " + token

stats = msf_msgrpc.moduleStats ()
print "Module Stats: " + str(stats)

response = msf_msgrpc.createConsole()
consoleId = response["id"]

print "Create Console: " + str(response)

response = msf_msgrpc.consoleRead(consoleId)
print "Console Read: " + str(response)

response = msf_msgrpc.consoleWrite(consoleId, "hosts")
print "Console Write: " + str(response)

response = msf_msgrpc.consoleRead(consoleId)
print "Console Read: " + str(response)

response = msf_msgrpc.destroyConsole(consoleId)
print "Destroy Console: " + str(response)