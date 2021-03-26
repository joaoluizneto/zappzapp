import socket, json

class ChatConnector:
    def __init__(self):
        with open('config.json', 'r', encoding='utf-8') as config:
            config = json.loads(config.read())
        
        self.clientIP = config['ChatConnectorConfig']['clientIP'] # ni.ifaddresses('eth0')[AF_INET][0]['addr']
        self.clientPort = config['ChatConnectorConfig']['clientPort']
        self.peerIP = config['ChatConnectorConfig']['peerIP'] # ni.ifaddresses('eth0')[AF_INET][0]['addr']
        self.peerPort = config['ChatConnectorConfig']['peerPort']
        self.username = config['ChatConnectorConfig']['username']

        self.serverIP = config['ChatConnectorConfig']['serverIP']
        self.serverPort = config['ChatConnectorConfig']['serverPort']

        self.clientsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.clientsock.bind((self.clientIP, self.clientPort))

    def subscribeToServer(self):
        #try:
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
        subscribed = self.clientsock.recvfrom(1024)[0].decode('utf-8')
        print(subscribed)
        #except:
            #print("Erro ao se conectar com o Servidor de Contatos.")

    def getContactDict(self):
        print('getting contacts...')
        requisition = json.dumps(
            {
                'req':'sendContactList',
                'arg': None,
                'usr': self.username
            })
        self.clientsock.sendto(requisition.encode(),(self.serverIP, self.serverPort))
        message = self.clientsock.recvfrom(1024)[0].decode('utf-8')
        response = json.loads(message)
        print(response)
        return response

    def stayConnectedLoop(self):
        while True:
            print("waiting for new status check")
            statuscheckreq= json.loads(self.clientsock.recvfrom(1024)[0].decode('utf-8'))
            if statuscheckreq['req'] == 'AreUoK':
                message = json.dumps({'status':'online'})
                self.clientsock.sendto(message.encode(),(self.serverIP, self.serverPort))
            

if __name__ == '__main__':
    objChatConnector = ChatConnector()
    objChatConnector.subscribeToServer()
    objChatConnector.getContactDict()