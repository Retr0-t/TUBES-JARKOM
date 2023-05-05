import socket
import os

def receive_http_request(conn):
    # Receive the data in small chunks and retransmit it
    data = b''
    while True:
        chunk = conn.recv(1024)
        if not chunk:
            break
        data += chunk
        if b'\r\n\r\n' in data:
            break
    return data.decode('utf-8')

def create_http_response(file_content):
    response_header = 'HTTP/1.1 200 OK\r\n'
    response_header += 'Content-Type: text/html; charset=UTF-8\r\n'
    response_header += '\r\n'
    response_body = file_content
    response = response_header + response_body
    return response.encode('utf-8')

def create_not_found_response():
    response_header = 'HTTP/1.1 404 Not Found\r\n'
    response_header += 'Content-Type: text/html; charset=UTF-8\r\n'
    response_header += '\r\n'
    response_body = '<h1>404 Not Found</h1>'
    response = response_header + response_body
    return response.encode('utf-8')

def get_file_content(filename):
    if not os.path.isfile(filename):
        return None
    with open(filename, 'rb') as f:
        file_content = f.read()
    return file_content

def handle_request(request):
    lines = request.split('\r\n')
    filename = ''
    for line in lines:
        if line.startswith('GET'):
            filename = line.split(' ')[1]
    filename = filename.lstrip('/')
    file_content = get_file_content(filename)
    if file_content is None:
        response = create_not_found_response()
    else:
        response = create_http_response(file_content)
    return response

def run_client():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('localhost', 8080)
    print(f"Connecting to {server_address[0]} port {server_address[1]}")
    sock.connect(server_address)

    # Send request to server
    http_request = "GET /index.html HTTP/1.1\r\nHost: localhost:8080\r\nConnection: keep-alive\r\n\r\n"
    print(f"Sending request:\n{http_request}")
    sock.sendall(http_request.encode('utf-8'))

    # Receive response from server and handle it
    http_response = receive_http_request(sock)
    print(f"Received response:\n{http_response}")
    response = handle_request(http_response)
    print(f"Sending response:\n{response}")
    sock.sendall(response)

    # Close the socket
    print("Closing socket")
    sock.close()

if __name__ == "__main__":
    run_client()
