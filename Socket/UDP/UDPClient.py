from socket import *
class UDPClient:
    serverName = "127.0.0.1"
    serverPort = 12000

    def run(self):
        client = socket(AF_INET,SOCK_DGRAM)#用户数据报
        message = input('请输入消息：')
        client.connect((self.serverName,self.serverPort))
        client.sendto(bytes(message,'utf-8'),(self.serverName,self.serverPort))
        data = client.recv(1024)
        print("客户端:对方回复："+str(data,encoding='utf-8'))
        client.close()
        print("客户端:结束连接")



if __name__=="__main__":
        client = UDPClient()
        client.run()