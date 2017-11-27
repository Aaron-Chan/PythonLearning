from socket import *


class UDPServer:
    HOST = ''
    PORT = 12000

    def run(self):
        server = socket(AF_INET, SOCK_DGRAM)
        print("服务器:开始绑定。。。")
        server.bind((self.HOST, self.PORT))
        print("服务器:开始监听。。。")
        # server.listen()
        while True:
            message, clientAddress = server.recvfrom(1024)
            print("服务器:收到%s的信息-%s" % (clientAddress,str(message,encoding='utf-8')))
            #server.sendto(data=bytes('我收到你的消息了',encoding='utf-8'),address=clientAddress)
            server.sendto(bytes('我收到你的消息了',encoding='utf-8'),clientAddress)



if __name__ == "__main__":
    server = UDPServer()
    server.run()
