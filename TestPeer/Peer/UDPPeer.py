import socket, json, queue, threading, time, os
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

        self.confirmedQ={}
        self.fileMsgList=[]

        #generator
        self.writeToFileGen = None
        self.genToken = True #available

    #set chatPage to update
    def setCurrentChatPage(self, objChatPage):
        self.objChatPage = objChatPage

    #refresh chatPage for the changed chat
    def updateCurrentChatPage(self,objChat=None):
        self.objChatPage.setChat(objChat=objChat)

    def routeMsgToChatObj(self, mensagem):
        try:
            mensagem = json.loads(mensagem)
        except json.decoder.JSONDecodeError:
            print("Json decode error")
            return
        firstkey = list(mensagem.keys())[0]
        if firstkey == "oriusername":
            self.sendConfirmation(mensagem)
            if mensagem["contenttype"]=="text":
                chatID = mensagem['chatID']

                if chatID in [chat.chatID for chat in self.objChatManager.chatList]:
                    pass
                else:
                    print("Adicionando Chat: ", mensagem['chatName'], mensagem['destUsers'], mensagem['chatID'])
                    objChat=self.objChatManager.addChat(mensagem['chatName'], mensagem['destUsers'], mensagem['chatID'])
                    self.updateCurrentChatPage(objChat=objChat)
                    self.objChatManager.saveChatList()
                    
                for chat in self.objChatManager.chatList:
                    if chat.chatID == chatID:
                        chat.addMessage(mensagem)
                        self.updateCurrentChatPage(objChat=chat)
            else:
                self.receiveFile(mensagem)

        elif firstkey == "confirmation":
            print("Removing confirmated: ", mensagem)
            confirmation = mensagem["confirmation"]
            confkey = list(confirmation.keys())[0]
            try:
                self.confirmedQ.pop(confkey)
            except KeyError:
                print(confkey+" already confirmed!")

    #updates new messages to each chat
    def routeMsgToChatObjLoop(self):
        while True:
            print("waiting for messages") # {'req':'subscribeUser', 'arg':{import:info}}
            mensagem = self.peersock.recvfrom(2024)[0].decode('utf-8')

            print("Message Received: ", mensagem)
            t  = threading.Thread(target=self.routeMsgToChatObj, args=(mensagem,))
            print("initializing thread for handling the received messages")
            t.start()


    def handleReceive(self):
        t  = threading.Thread(target=self.routeMsgToChatObjLoop, args=())
        print("initializing thread for waiting receive")
        t.start()

    def receiveFile(self,message):
        #generator to deal with saving file
        while True:
            if self.genToken: #se nõ tem ninguém usndo o gerador
                self.genToken= False #bloqueia gerador
                if self.writeToFileGen:
                    try:
                        self.writeToFileGen.send(message)
                    except StopIteration:
                        print("Stopped writing")
                        #self.writeToFileGen = self.writeToFile(message)
                        #self.writeToFileGen.send(None)
                        #self.writeToFileGen.send(message)
                        
                else:
                    self.writeToFileGen = self.writeToFile(message)
                    self.writeToFileGen.send(None)
                    self.writeToFileGen.send(message)
                self.genToken= True #desblloqueia gerador
                break
            else:
                pass


    def writeToFile(self, message):
        count=0
        chunks=[]
        with open("./DownloadFile/"+message["filename"], "wb") as f:
            finish=False
            while True:
                message = yield
                if message:
                    if message["filesize"]>0:
                        print("Writing chunck:", message["msgNumber"])
                        f.write(message["content"].encode())
                        chunks.append(message["msgNumber"])
                    else:
                        print("Stoping writing...")
                        finish = True
                        self.writeToFileGen=None
                        break
                        if finish and max(chunks)==(len(chunks)-1):
                            print(chunks)
                            print("Parando escrita!")
                            break
                        count+=1
                else:
                    continue

    def getUserAddr(self, username):
        contactDict = self.objChatConnector.getContactDict()
        try:
            resp = (contactDict[username]['peerIP'], int(contactDict[username]['peerPort']))
        except KeyError:
            resp = None
        return resp

    def sendMessage(self,message):
        destUsers = message['destUsers']
        for user in destUsers:
            userAddr = self.getUserAddr(user)
            if userAddr:
                self.peersock.sendto((json.dumps(message)).encode(), userAddr)
                self.confirmedQ[user+str(message["msgNumber"])+message["senttime"]]=(message, user, "not confirmed")
                                         
            else:
                print(user+" not subscribed!")

    def resendMessage(self,message,user):
        userAddr = self.getUserAddr(user)
        if userAddr:
            print("resending message: ")
            self.peersock.sendto((json.dumps(message)).encode(), userAddr)
            #self.confirmedQ.append((message, user, "not confirmed"))
        else:
            print(user+" not subscribed!")

    def sendConfirmation(self,message):
        user = message["oriusername"]
        userAddr = self.getUserAddr(user)
        if userAddr:
            message = {"confirmation":{self.objChatConnector.username+str(message["msgNumber"])+message["senttime"]:
                                         (self.objChatConnector.username, "confirmed")}}
            self.peersock.sendto((json.dumps(message)).encode(), userAddr)
        else:
            print(user+" not subscribed!")

    def checkConfirmations(self):
        while True:
            time.sleep(5)
            #print("Dict Confirm: ", self.confirmedQ)
            try:
                for notconfirmed in self.confirmedQ:
                    print("Not confirmed: ",len(self.confirmedQ))
                    print("Resending not confirmed message: "+notconfirmed)
                    self.resendMessage(self.confirmedQ[notconfirmed][0], self.confirmedQ[notconfirmed][1])
            except RuntimeError:
                print("Deu xabu, vamo de novo...")
                continue

    def handleConfirmation(self):
        t  = threading.Thread(target=self.checkConfirmations, args=())
        print("initializing thread for handling confirmed messages")
        t.start()

    def handleSndFile(self, objChat, path='./UploadFile/'):
        t  = threading.Thread(target=self.sndFile, args=(objChat, path))
        print("initializing thread for handling send file")
        t.start()

    def sndFile(self, objChat, path='./UploadFile/'):
        #break file into message list
        filesize = os.path.getsize(path)
        print("filesize: ", filesize)
        with open(path, 'rb') as f:
            count=0
            while True:
                # read the bytes from the file
                bytes_read = f.read(1000)
                if not bytes_read:
                    # file transmitting is done
                    print("file transmiting is over!")
                    msg = objChat.createMsg('file', "None")
                    msg["filename"]=path.split("/")[len(path.split("/"))-1]
                    msg["content"]=None
                    msg["filesize"]=0
                    self.sendMessage(msg)
                    break
                msg = objChat.createMsg('file', "content")
                msg["filename"]=path.split("/")[len(path.split("/"))-1]
                msg["content"]=bytes_read.decode("utf-8")
                msg["filesize"]=filesize
                msg["msgNumber"]=count
                count+=1
                #print("MessageFile: ", msg)
                # we use sendall to assure transimission in 
                # busy networks

                self.sendMessage(msg)
                #print("Sent Msg: ", msg["msgNumber"])
                time.sleep(0.2)
                # update the progress bar

        #send message by message showing progress



if  __name__ == "__main__":
    pass
