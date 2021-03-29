import socket, json, queue, threading
import ChatConnector
import Chat

class UDPPeer:
    def __init__(self, objChatManager, objChatConnector):

        self.objChatConnector = objChatConnector
        self.objChatManager = objChatManager

        self.peerIP = objChatConnector.peerIP # ni.ifaddresses('eth0')[AF_INET][0]['addr']
        self.peerPort = objChatConnector.peerPort

        self.peersock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.peersock.bind((self.peerIP, self.peerPort))

    #set chatPage to update
    def setCurrentChatPage(self, objChatPage):
        self.objChatPage = objChatPage

    #refresh chatPage for the changed chat
    def updateCurrentChatPage(self):
        self.objChatPage.setChat()

    #updates new messages to each chat
    def routeMsgToChatObjLoop(self):
        while True:
            print("waiting for messages") # {'req':'subscribeUser', 'arg':{import:info}}
            mensagem = self.peersock.recvfrom(1024)[0].decode('utf-8')
            mensagem = json.loads(mensagem)
            chatID = mensagem['chatID']
            for chat in self.objChatManager.chatList:
                if chat.chatID == chatID:
                    chat.addMessage(mensagem)
                    self.updateCurrentChatPage()

    def handleReceive(self):
        t  = threading.Thread(target=self.routeMsgToChatObjLoop, args=())
        print("initializing thread for handling the received messages")
        t.start()

    def getUserAddr(self, username):
        contactDict = self.objChatConnector.getContactDict()
        try:
            resp = (contactDict[username]['peerIP'], int(contactDict[username]['peerPort']))
        except KeyError:
            resp = None
        return resp

    def sendMessage(self,message):
        chatID = message['chatID']
        for chat in self.objChatManager.chatList:
            if chat.chatID == chatID:
                destUsers = chat.destUsers
        for user in destUsers:
            userAddr = self.getUserAddr(user)
            if userAddr:
                self.peersock.sendto((json.dumps(message)).encode(), userAddr)
            else:
                print(user+" not subscribed!")
