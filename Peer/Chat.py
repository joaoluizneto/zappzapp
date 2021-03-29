import uuid, time, json
import ChatConnector

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
        with open('messageList.json', 'r') as messageList:
            messageList = json.loads(messageList.read())
            for msgNumber in messageList:
                if messageList[msgNumber]['chatID']==self.chatID:
                    self.messageList.append(messageList[msgNumber])

        
    def toJson(self):
        dictChat={
            str(self.chatID):{
                'chatName':self.chatName,
                'destUsers':self.destUsers
            }
        }
        jsonChat = json.dumps(dictChat)
        return jsonChat


    def createMsg(self, contenttype, content):
        msgDict={
            "oriusername":self.objChatConnector.username,
            "msgNumber":len(self.messageList),
            "chatID": self.chatID,
            "senttime": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            "contenttype": contenttype,
            "content": content
        }
        return msgDict

    def addMessage(self, message):
        self.messageList.append(message)
        print(self.messageList)

    def sndMsgToUpload(self, contenttype, content):
        msgJson = self.createMsg(contenttype, content)
        return msgJson

