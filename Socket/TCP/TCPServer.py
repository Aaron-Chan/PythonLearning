from socket import *


class TCPServer:
    HOST = ''
    PORT = 14000

    def run(self):
        server = socket(AF_INET, SOCK_STREAM)
        print("TCP服务器:开始绑定。。。")
        server.bind((self.HOST, self.PORT))
        server.listen(1)
        print("TCP服务器:开始监听。。。")
        # server.listen()
        while True:
            connectionSocket,clientAddress=server.accept()
            message = connectionSocket.recv(1024)
            print("TCP服务器:收到%s的信息-%s" % (clientAddress,message))
            connectionSocket.send(b'received')
            connectionSocket.close()


if __name__ == "__main__":
    server = TCPServer()
    server.run()
