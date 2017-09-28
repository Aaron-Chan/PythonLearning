# -*- coding:utf-8 -*-
import http.server
import posixpath
import urllib.parse
import mimetypes
import os





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
        self.send_head();

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(len(self.Page)))
        self.end_headers()

        self.wfile.write(self.Page.encode())

    def do_HEAD(self):
        # 处理当前的路径
        path = self.translate_path(self.path)

        super().do_HEAD()

    def send_head(self):
        path = self.translate_path(self.path)
        if not (os.path.isdir(path)):  # 重定向
            if not path.endswith('/'):
                self.send_response(301)
                self.send_header("Location", self.path + "/")
                self.end_headers()
                return None
            for index in {"index.html","index.htm"}:
                tempPath = os.path.join(path,index)
                if os.path.exists(tempPath):
                    path = tempPath
                    break
            else:
               return self.list_directory(path)
        fileType = mimetypes.guess_type(path)
        os.open(path)
        self.send_header("Content")


        # 获取文件类型 文件长度

    def translate_path(self, path):
        """转换地址"""

        print("handle before path:%s" % self.path)
        # 去除查询参数
        path = path.split('?', 1)[0]
        path = path.split('#', 1)[0]
        path = posixpath.normpath(urllib.parse.unquote(path))
        words = path.split('/')
        words = [_f for _f in words if _f]
        path = os.getcwd()
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir): continue
            path = os.path.join(path, word)
        print("handle after path:%s" % self.path)
        return path


# 1.完成do get协议  罗列文件表
# 2.完成下载的工作
# 3.上传工作




def run(server_class=http.server.HTTPServer, handler_class=RequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == '__main__':
    run()
