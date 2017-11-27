from  socket import *
class TCPClient:
    HOST='127.0.0.1'
    PORT=14000

    def run(self):
        client=socket(AF_INET,SOCK_STREAM)
        client.connect((self.HOST,self.PORT))
        message = input('请输入信息：')
        client.send(bytes(message,encoding='utf-8'))
        data=client.recv(1024)
        print('返回的信息：%s'%str(data,encoding='utf-8'))
        client.close()
        print("客户端:结束连接")


if __name__=='__main__':
    client = TCPClient()
    client.run()

