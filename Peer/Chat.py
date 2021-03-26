import uuid, time, json

class Chat:
    def __init__(self):
        with open('config.json', 'r', encoding='utf-8') as config:
            config = json.loads(config.read())
        self.myusername = config['ChatConnectorConfig']['username']
        self.messageList = [] #lista de jsons
        self.destUsers = [] #lista de usernames
        self.chatID = str(uuid.uuid4()) #id unico

    def createMsg(self, contenttype, content):
        global objChatConnector
        msgDict={
            "oriusername":self.myusername,
            "msgNumber":len(self.messageList),
            "chatID": self.chatID,
            "senttime": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            "contenttype": contenttype,
            "content": content
        }
        msgJson = json.dumps(msgDict)
        return msgJson

    def sndMsgToUpload(self, contenttype, content):
        msgJson = self.createMsg(contenttype, content)

