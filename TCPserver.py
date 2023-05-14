import socket
import os

# Mengatur alamat dan port server
alamat_server = 'localhost'  # Alamat IP loopback untuk server lokal
port_server = 8080  # Port yang akan digunakan oleh server

# Mendapatkan direktori kerja saat ini
current_directory = os.getcwd()

# Menentukan lokasi file "index.html"
index_html_path = os.path.join(current_directory, 'C:\\Users\\ASUS\\Downloads\\SEMESTER 4\\JARKOM PRAK\\TUBES SERVER\\index.html')

# Membaca isi file "index.html"
with open(index_html_path, 'r') as file:
    content = file.read()

# Membuat objek socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Mengaitkan socket dengan alamat dan port
sock.bind((alamat_server, port_server))

# Mendengarkan koneksi masuk
sock.listen(1)  # Hanya satu koneksi yang dapat di-queue

print("Server TCP siap untuk menerima koneksi.")

while True:
    # Menerima koneksi dari client
    conn, addr = sock.accept()

    print(f"Menerima koneksi dari: {addr[0]}:{addr[1]}")

    # Menerima data dari client
    data = conn.recv(1024).decode('utf-8')
    print(f"Data yang diterima: {data}")

    # Memeriksa jika permintaan adalah GET /index.html
    if "GET /" in data:
        # Mengirimkan konten HTML ke client
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + content
    else:
        # Mengirimkan respons 404 - Page Not Found
        response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\n404 - Page Not Found"

    # Mengirimkan respons ke client
    conn.sendall(response.encode('utf-8'))

    # Menutup koneksi dengan client
    conn.close()
