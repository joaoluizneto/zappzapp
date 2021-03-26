import socket, json
from netifaces import AF_INET, AF_INET6, AF_LINK, AF_PACKET, AF_BRIDGE
import netifaces as ni

import ChatConnector

class UDPPeer:
    def __init__(self):
        with open('config.json', 'r', encoding='utf-8') as config:
            config = json.loads(config.read())
        
        self.peerIP = config['UDPPeerConfig']['peerIP'] # ni.ifaddresses('eth0')[AF_INET][0]['addr']
        self.peerPort = config['UDPPeerConfig']['peerPort']

        self.peersock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.peersock.bind((self.peerIP, self.peerPort))

    def getUserAddr(self, objChatConnector, username):
        contactDict = objChatConnector.getContactDict()
        return (contactDict[username]['peerIP'], contactDict[username]['peerPort'])

if __name__ == '__main__':
    objChatConnector = ChatConnector.ChatConnector()
    objUDPPeer = UDPPeer()
    print(objUDPPeer.getUserAddr(objChatConnector, 'username3'))
