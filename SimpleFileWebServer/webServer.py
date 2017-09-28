# -*- coding:utf-8 -*-
import http.server


class RequestHandler(http.server.SimpleHTTPRequestHandler):
    # Page to send back.
    Page = '''\
    <html>
    <body>
    <p>Hello, web!</p>
    </body>
    </html>
    '''

    def do_GET(self):
        print("Just received a GET request")
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(len(self.Page)))
        self.end_headers()
        self.wfile.write(bytes(self.Page,'utf-8'))

# 1.完成doget协议  罗列文件表
# 2.完成下载的工作
# 3.上传工作
    



def run(server_class=http.server.HTTPServer, handler_class=RequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == '__main__':
    run()
