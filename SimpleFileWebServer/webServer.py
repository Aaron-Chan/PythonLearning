# -*- coding:utf-8 -*-
import cgi
import http.server
import posixpath
import urllib.parse
import mimetypes
import os
import shutil
from http import HTTPStatus
from pydoc import html

import sys

from io import BytesIO


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
       f= self.send_head()
       if f:
           shutil.copyfileobj(f,self.wfile)
           f.close()

        # self.send_response(200)
        # self.send_header("Content-type", "text/html")
        # self.send_header("Content-Length", str(len(self.Page)))
        # self.end_headers()
        #
        # self.wfile.write(self.Page.encode())

    def do_HEAD(self):
        # 处理当前的路径
        f = self.send_head()
        if f:
            f.close()

    def send_head(self):
        path = self.translate_path(self.path)
        if  (os.path.isdir(path)):  # 重定向
            if not self.path.endswith('/'):
                self.send_response(HTTPStatus.MOVED_PERMANENTLY)
                self.send_header("Location", self.path + "/")
                self.end_headers()
                return None
            for index in {"index.html", "index.htm"}:
                tempPath = os.path.join(path, index)
                if os.path.exists(tempPath):
                    path = tempPath
                    break
            else:
                return self.list_directory(path)
        fileType = mimetypes.guess_type(path)
        try:
            f = open(path, 'rb')
        except IOError:
            self.send_error(404, "File not found")
            return None

        self.send_header("Content-type", fileType)
        self.send_header("Content-Length", os.stat(path).st_size)
        self.send_header("Last-Modified", self.date_time_string(os.stat(path).st_mtime))
        self.end_headers()
        return f

    def list_directory(self,path):
        """Helper to produce a directory listing (absent index.html).

               Return value is either a file object, or None (indicating an
               error).  In either case, the headers are sent, making the
               interface the same as for send_head().

               """
        try:
            list = os.listdir(path)
        except OSError:
            self.send_error(
                HTTPStatus.NOT_FOUND,
                "No permission to list directory")
            return None
        list.sort(key=lambda a: a.lower())
        r = []
        try:
            displaypath = urllib.parse.unquote(self.path,
                                               errors='surrogatepass')
        except UnicodeDecodeError:
            displaypath = urllib.parse.unquote(path)

        displaypath = cgi.escape(urllib.parse.unquote(displaypath))
        enc = sys.getfilesystemencoding()
        title = 'Directory listing for %s' % displaypath
        r.append('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" '
                 '"http://www.w3.org/TR/html4/strict.dtd">')
        r.append('<html>\n<head>')
        r.append('<meta http-equiv="Content-Type" '
                 'content="text/html; charset=%s">' % enc)
        r.append('<title>%s</title>\n</head>' % title)
        r.append('<body>\n<h1>%s</h1>' % title)
        # 上传
        r.append('<hr>\n')
        r.append('<form ENCTYPE=\"multipart/form-data\" method=\"post\">')
        r.append('<input name=\"file\" type=\"file\"/>')
        r.append('<input type=\"submit\" value=\"upload\"/></form>\n')

        r.append('<hr>\n<ul>')
        for name in list:
            fullname = os.path.join(path, name)
            displayname = linkname = name
            # Append / for directories or @ for symbolic links
            if os.path.isdir(fullname):
                displayname = name + "/"
                linkname = name + "/"
            if os.path.islink(fullname):
                displayname = name + "@"
                # Note: a link to a directory displays with @ and links with /
            r.append('<li><a href="%s">%s</a></li>'
                     % (urllib.parse.quote(linkname,
                                           errors='surrogatepass'),
                        cgi.escape(urllib.parse.unquote(displayname))))
        r.append('</ul>\n<hr>\n</body>\n</html>\n')
        encoded = '\n'.join(r).encode(enc, 'surrogateescape')
        f = BytesIO()
        f.write(encoded)
        f.seek(0)
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "text/html; charset=%s" % enc)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        return f

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
