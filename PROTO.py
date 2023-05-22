import socket
import os

def change_directory():
    os.chdir("C:\\Users\\ASUS\\Downloads\\SEMESTER 4\\JARKOM PRAK\\TUBES SERVER")

# Mengatur alamat dan port server
alamat_server = 'localhost'  # Alamat IP loopback untuk server lokal
port_server = 8080  # Port yang akan digunakan oleh server

# Mendapatkan direktori kerja saat ini
current_directory = os.getcwd()

# Membaca isi file "index.html"
index_html_path = os.path.join(current_directory, 'index.html')

# Membaca isi file "style.css"
css_path = os.path.join(current_directory, 'index.css')

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
    data = conn.recv(1024).decode('latin-1')
    print(f"Data yang diterima: {data}")

    # Menyimpan data yang diterima ke file
    with open('received_data.txt', 'w') as file:
        file.write(data)

    # Memeriksa jika permintaan adalah GET /
    if "GET /" in data:
        change_directory()  # Panggil fungsi untuk berpindah ke direktori yang ditentukan
        
        # Membaca isi file "index.html"
        with open(index_html_path, 'r') as file:
            content = file.read()

        # Membaca isi file "style.css"
        with open(css_path, 'r') as file:
            css_content = file.read()
        
        # Menyusun respons HTTP
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + content

        # Menambahkan CSS ke respons
        response += "\r\n<style>\r\n" + css_content + "\r\n</style>\r\n"
    else:
        # Mengirimkan respons 404 - Page Not Found
        response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\n404 - Page Not Found"

    # Mengirimkan respons ke client
    conn.sendall(response.encode('utf-8'))

    # Menutup koneksi dengan client
    conn.close()
