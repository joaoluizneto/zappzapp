import socket, json, time, threading

class ContactServer:
    def __init__(self):
        with open('serverconfig.json', 'r', encoding='utf-8') as config:
            self.config = json.loads(config.read())
        self.serverIP = self.config['ContactServerConfig']['serverIP'] # ni.ifaddresses('eth0')[AF_INET][0]['addr']
        self.serverPort = self.config['ContactServerConfig']['serverPort']

        self.contactDict = {} # [ip, username, clientport, status]
        self.serversock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.serversock.bind((self.serverIP, self.serverPort))

        self.threadList = []

    def subscribeUser(self, subsinfo, username):
        print("subscribing user: "+username)
        username=list(subsinfo.keys())[0]

        subsexists=False
        if username in self.contactDict:
            subsexists=True
        if not subsexists:
            print("subscribing: ",subsinfo)
            self.contactDict[username] = subsinfo[username]
            self.serversock.sendto("Subscribed".encode(), (subsinfo[username]['clientIP'], subsinfo[username]['clientPort']))
        else: # o usuário já cadastrado é vc mesmo?
            message="user "+username+" already subscribed! updated..."
            print(message)
            self.contactDict[username] = subsinfo[username]
            self.serversock.sendto(message.encode(), (subsinfo[username]['clientIP'], subsinfo[username]['clientPort']))

    def verifyContactsStatusLoop(self):
        print("verifyContactsStatusLoop initiated")
        while True:
            for username in self.contactDict:
                print("getting "+username+" status")
                message = requisition = json.dumps(
                    {
                        'req':'AreUoK',
                    })
                self.serversock.sendto(message.encode(), (self.contactDict[username]['clientIP'], self.contactDict[username]['clientPort']))
                try:
                    response={'status':'offline'}
                    self.serversock.settimeout(5)
                    response = json.loads(self.serversock.recvfrom(1024)[0].decode('utf-8'))
                    self.contactDict[username]['status'] = response['status']
                    self.serversock.settimeout(None)
                except socket.timeout:
                    print("statuscheck timeout")
                    self.contactDict[username]['status'] = response['status']
                print(response)
            time.sleep(5)

    def sendContactList(self, arg, username):
        print("sending contactDict...")
        message = json.dumps(self.contactDict)
        self.serversock.sendto(message.encode(), (self.contactDict[username]['clientIP'], self.contactDict[username]['clientPort']))

    def hadleReqLoop(self):
        requisitionMethods = {'subscribeUser':self.subscribeUser, 'sendContactList':self.sendContactList}
        while True:
            print("waiting for requisitions") # {'req':'subscribeUser', 'arg':{import:info}}
            mensagem = self.serversock.recvfrom(1024)[0].decode('utf-8')
            requisition = json.loads(mensagem)
            self.handleReq(requisition)

             
    def handleReq(self, requisition):
        requisitionMethods = {'subscribeUser':self.subscribeUser, 'sendContactList':self.sendContactList}
        req = requisition['req']
        arg = requisition['arg']
        usr = requisition['usr']
        print("new requisition: ", requisition, " from "+str(usr))
        #requisitionMethods[req](arg, usr)
        t  = threading.Thread(target=requisitionMethods[req], args=(arg, usr))
        print("initializing thread for handling the request")
        t.start()
        #self.threadList.append(t)
             
    def saveToMemory():
        pass


if __name__ == '__main__':
    objContactServer = ContactServer()
    objContactServer.hadleReqLoop()
