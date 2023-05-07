#Baris ini mengimpor modul HTTPServer dan BaseHTTPRequestHandler dari library http.server.
from http.server import HTTPServer, BaseHTTPRequestHandler

#Baris ini mendefinisikan kelas Serv yang merupakan subclass dari BaseHTTPRequestHandler.
class Serv(BaseHTTPRequestHandler):

#Ini adalah metode dalam kelas Serv, yang akan dipanggil ketika permintaan GET diterima.
    def do_GET(self):

#Ini adalah kondisi untuk mengubah path menjadi '/index.html' jika permintaan tidak mencantumkan path.
        if self.path == '/':
            self.path = '/index.html'

# Ini mencoba membuka file yang diminta, 
# jika berhasil maka akan mengirimkan respon dengan kode 200 OK, 
# dan jika gagal maka akan mengirimkan respon dengan kode 404 Not Found.
        try:
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
        except:
            file_to_open = "File not found"
            self.send_response(404)
    
#Ini mengakhiri header HTTP dan menulis isi file yang diminta ke output.
        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))


#Ini membuat instance dari HTTPServer dan mendefinisikan port dan handler untuk permintaan HTTP, 
# kemudian memanggil metode serve_forever() untuk menjalankan server secara terus-menerus.
httpd = HTTPServer(('localhost', 8080), Serv)
httpd.serve_forever()