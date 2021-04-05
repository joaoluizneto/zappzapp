import socket, json
from tkinter.constants import S

class ChatConnector:
    def __init__(self, peerIP=None, peerPort=None, username=None, clientIP=None, clientPort=None, serverIP=None, serverPort=None):
        self.clientsock=None
        with open('config.json', 'r', encoding='utf-8') as config:
            config = json.loads(config.read())

        if not clientIP:
            self.clientIP = config['ChatConnectorConfig']['clientIP'] # ni.ifaddresses('eth0')[AF_INET][0]['addr']
        else:
            config['ChatConnectorConfig']['clientIP'] = clientIP
            self.clientIP = clientIP

        if not clientPort:
            self.clientPort = config['ChatConnectorConfig']['clientPort']
        else:
            config['ChatConnectorConfig']['clientPort'] = clientPort
            self.clientPort = clientPort

        if not peerIP:
            self.peerIP = config['ChatConnectorConfig']['peerIP'] # ni.ifaddresses('eth0')[AF_INET][0]['addr']
        else:
            config['ChatConnectorConfig']['peerIP'] = peerIP
            self.peerIP = peerIP

        if not peerPort:
            self.peerPort = int(config['ChatConnectorConfig']['peerPort'])
        else:
            config['ChatConnectorConfig']['peerPort'] = peerPort
            self.peerPort = int(peerPort)

        if not username:
            self.username = config['ChatConnectorConfig']['username']
        else:
            config['ChatConnectorConfig']['username'] = username
            self.username = username

        if not serverIP:
            self.serverIP = config['ChatConnectorConfig']['serverIP']
        else:
            config['ChatConnectorConfig']['serverIP'] = serverIP
            self.serverIP = serverIP

        if not serverPort:
            self.serverPort = int(config['ChatConnectorConfig']['serverPort'])
        else:
            config['ChatConnectorConfig']['serverPort'] = serverPort
            self.serverPort = int(serverPort)

        with open('config.json', 'w', encoding='utf-8') as saveconfig:
            #print("ChatConnectorConfig: ")
            #print(config)
            config = json.dumps(config)
            saveconfig.write(config)

    def setConfig(self, peerIP=None, peerPort=None, username=None, clientIP=None, clientPort=None, serverIP=None, serverPort=None):
        with open('config.json', 'r', encoding='utf-8') as config:
            config = json.loads(config.read())

        if not clientIP:
            self.clientIP = config['ChatConnectorConfig']['clientIP'] # ni.ifaddresses('eth0')[AF_INET][0]['addr']
        else:
            config['ChatConnectorConfig']['clientIP'] = clientIP
            self.clientIP = clientIP

        if not clientPort:
            self.clientPort = config['ChatConnectorConfig']['clientPort']
        else:
            config['ChatConnectorConfig']['clientPort'] = clientPort
            self.clientPort = clientPort

        if not peerIP:
            self.peerIP = config['ChatConnectorConfig']['peerIP'] # ni.ifaddresses('eth0')[AF_INET][0]['addr']
        else:
            config['ChatConnectorConfig']['peerIP'] = peerIP
            self.peerIP = peerIP

        if not peerPort:
            self.peerPort = int(config['ChatConnectorConfig']['peerPort'])
        else:
            config['ChatConnectorConfig']['peerPort'] = peerPort
            self.peerPort = int(peerPort)

        if not username:
            self.username = config['ChatConnectorConfig']['username']
        else:
            config['ChatConnectorConfig']['username'] = username
            self.username = username

        if not serverIP:
            self.serverIP = config['ChatConnectorConfig']['serverIP']
        else:
            config['ChatConnectorConfig']['serverIP'] = serverIP
            self.serverIP = serverIP

        if not serverPort:
            self.serverPort = int(config['ChatConnectorConfig']['serverPort'])
        else:
            config['ChatConnectorConfig']['serverPort'] = serverPort
            self.serverPort = int(serverPort)

        with open('config.json', 'w', encoding='utf-8') as saveconfig:
            #print("ChatConnectorConfig: ")
            #print(config)
            config = json.dumps(config)
            saveconfig.write(config)


    def subscribeToServer(self):
        #try:
        self.clientsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.clientsock.bind((self.clientIP, self.clientPort))

        requisition = json.dumps(
            {
                'req':'subscribeUser',
                'arg':
                    {
                        self.username:
                            {
                                'clientIP':self.clientIP,
                                'clientPort':self.clientPort,
                                'peerIP':self.peerIP,
                                'peerPort':self.peerPort,
                                'status':'online'
                            }
                    },
                'usr': self.username
            })
        self.clientsock.sendto(requisition.encode(),(self.serverIP, self.serverPort))
        try:
            self.clientsock.settimeout(5)
            subscribed = self.clientsock.recvfrom(1024)[0].decode('utf-8')
            self.clientsock.settimeout(5)
        except socket.timeout:
            print("subscribe timeout")
            subscribed = "Timeout"
        #print(str(subscribed))
        return subscribed
        #except:
            #print("Erro ao se conectar com o Servidor de Contatos.")

    def getContactDict(self):
        if not self.clientsock:
            self.clientsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.clientsock.bind((self.clientIP, self.clientPort))
        #print('getting contacts... ')
        requisition = json.dumps(
            {
                'req':'sendContactList',
                'arg': None,
                'usr': self.username
            })
        #print(requisition)
        self.clientsock.sendto(requisition.encode(),(self.serverIP, self.serverPort))
        message = self.clientsock.recvfrom(1024)[0].decode('utf-8')
        response = json.loads(message)
        #print(response)
        return response

    def stayConnectedLoop(self):
        while True:
            print("waiting for new status check")
            statuscheckreq= json.loads(self.clientsock.recvfrom(1024)[0].decode('utf-8'))
            if statuscheckreq['req'] == 'AreUoK':
                message = json.dumps({'status':'online'})
                self.clientsock.sendto(message.encode(),(self.serverIP, self.serverPort))
            
