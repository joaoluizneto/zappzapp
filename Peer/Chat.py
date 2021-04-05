import uuid, time, json, os


class Chat:
    def __init__(self, objChatConnector, chatName=None, chatID=None, destUsers=None):
        with open('config.json', 'r', encoding='utf-8') as config:
            config = json.loads(config.read())

        self.objChatConnector = objChatConnector

        if not chatID:
            self.chatID = str(uuid.uuid4()) #id unico
        else:
            self.chatID = chatID

        if not chatName:
            self.chatName = self.chatID
        else:
            self.chatName = chatName

        if not destUsers:
            self.destUsers = [self.objChatConnector.username] #lista de usernames
        else:
            self.destUsers = destUsers

        self.messageList = [] #lista de jsons
        if not os.path.isfile(self.chatID+'messageList.json'):
            with open(self.chatID+'messageList.json', 'w') as messageList:
                messageList.write("{}")
        else:
            with open(self.chatID+'messageList.json', 'r') as messageList:
                messageList = json.loads(messageList.read())
                for message in messageList:
                    #if messageList[msgNumber]['chatID']==self.chatID:
                    self.messageList.append(message)

        
    def toJson(self):
        dictChat={
            str(self.chatID):{
                'chatName':self.chatName,
                'destUsers':self.destUsers
            }
        }
        jsonChat = json.dumps(dictChat)
        return jsonChat


    def createMsg(self, contenttype, content, msgNumber=None):
        if msgNumber == None: 
            msgNumber=len(self.messageList)
        msgDict={
            "oriusername":self.objChatConnector.username,
            "msgNumber":len(self.messageList),
            "chatID": self.chatID,
            "chatName": self.chatName,
            "destUsers": self.destUsers,
            "senttime": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            "contenttype": contenttype,
            "content": content
        }
        return msgDict

    def addMessage(self, message):
        self.messageList.append(message)
        with open(self.chatID+'messageList.json', 'w') as messageList:
            messageList.write(json.dumps(self.messageList))
        print(self.messageList)


