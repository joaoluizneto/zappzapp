import Chat, json, ChatConnector

class ChatManager:
    def __init__(self, objChatConnector):
        self.objChatConnector = objChatConnector
        #carrega chats do arquivo
        with open('chatList.json', 'r', encoding='utf-8') as chatList:
            chatList = json.loads(chatList.read())


        #instancia chats
        self.chatList = [Chat.Chat(objChatConnector,chatID=chatID,
                                    chatName=chatList[chatID]['chatName'],
                                    destUsers=chatList[chatID]['destUsers'])
                                     for chatID in chatList]

    def newChat(self, _chatName, _destUsers):
        newChat = Chat.Chat(self.objChatConnector, chatName=_chatName, destUsers=_destUsers)
        self.chatList.append(newChat)



    def addChat(self, _chatName, _destUsers, _chatID):
        newChat = Chat.Chat(self.objChatConnector,chatName=_chatName, destUsers=_destUsers, chatID=_chatID)
        self.chatList.append(newChat)


    def rmChat(self, ):
        pass

    def saveChatList(self):
        dictChat={}
        for objChat in self.chatList:
            dictChat[objChat.chatID] ={
                        "chatName":objChat.chatName,
                        "destUsers":objChat.destUsers
                    }
        with open('chatList.json', 'w', encoding='utf-8') as chatList:
            chatList.write(json.dumps(dictChat))


    def printChats(self):
        for chat in self.chatList:
            print(chat.toJson())

