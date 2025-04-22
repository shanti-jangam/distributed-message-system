import socket
import argparse

def forward_message(message, next_host, next_port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((next_host, next_port))
            s.sendall(message.encode('utf-8'))
            print(f"[SERVER-2] Message forwarded successfully to {next_host}:{next_port}")
    except Exception as e:
        print(f"[SERVER-2] Forward failed: {e}")

def start_server(port, next_hostport):
    host = ''
    next_host, next_port = next_hostport.split(':')
    next_port = int(next_port)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((host, port))
        server.listen()
        print(f"[SERVER-2] Listening on port {port}, will forward to {next_hostport}")
        conn, addr = server.accept()
        with conn:
            data = conn.recv(1024).decode('utf-8')
            print(f"[SERVER-2] Received message from {addr[0]}:{addr[1]}: {data}")
            forward_message(data, next_host, next_port)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', required=True, type=int)
    parser.add_argument('-n', required=True)
    args = parser.parse_args()
    start_server(args.l, args.n)
