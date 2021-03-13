import os
import sys
import nmap
import time
import re
import speech
import socket

try:
    nm = nmap.PortScanner()         # instance of nmap.PortScanner
except nmap.PortScannerError:
    print('Nmap not found', sys.exc_info()[0])
    sys.exit(0)
except:
    print("Unexpected error:", sys.exc_info()[0])
    sys.exit(0)

hostList = []
gracePeriod = 5
device_name = ''
device_count = 0
ipv4 = socket.gethostbyname_ex(socket.gethostname())[-1]
ipv4 = (ipv4[len(ipv4) -1])
ipv4 = str(ipv4.split('.')[0] + '.0.0/24')
running = False

def seek():
    global device_name
    global ipv4
    curHosts = []
    nm.scan(hosts = ipv4, arguments = '-n -sP -PE -T5')
    # executes a ping scan

    localtime = time.asctime(time.localtime(time.time()))
    print('============ {0} ============'.format(localtime))
    # system time
    
    for host in nm.all_hosts():
        try:
            mac = nm[host]['addresses']['mac']
            vendor = nm[host]['vendor'][mac]
        except:
            vendor = mac = 'unknown'

        curHosts.append((host,mac,vendor,gracePeriod))
    
    updateHostList(curHosts)

    for host in hostList:
        device_name = host[2]
        print('Scan report for %s\nMAC Address: %s (%s)' % (host[0], host[1], host[2]))

    print('Number of hosts: ' + str(len(hostList)))
    return len(hostList)                # returns count

def updateHostList(curHosts):
    global hostList
    if hostList == []:
        hostList = curHosts
    else:
        hostList = [(x[0],x[1],x[2],x[3]-1) for x in hostList]

        # only the hosts that were new in this iteration
        newList = [(x[0],x[1],x[2],x[3]) for x in curHosts if not (any(x[0]==y[0] for y in hostList))]

        for host in newList:
            hostList.append(host)

        for host in hostList:
            if any(host[0] == y[0] for y in curHosts):
                hostList[hostList.index(host)] = (host[0],host[1],host[2],gracePeriod)

        for host in hostList:
            if host[3] <= 0:
                hostList.remove(host)          

old_count = new_count = seek()
startCounter = gracePeriod

# are there any new hosts?
while running:
    startCounter -= 1
    time.sleep(1)               # increase to slow down the speed
    old_count = new_count
    new_count = seek()
    device_count = new_count

    # DANGER!!!
    if not ((new_count <= old_count) or startCounter >= 0) and not device_name == 'unknown':
        speech.say(device_name + ' device just connected to the network')
        time.sleep(4)