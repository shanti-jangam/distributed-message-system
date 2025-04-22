import socket
import argparse

def start_server(port):
    host = ''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((host, port))
        server.listen()
        print(f"[SERVER-3] Listening on port {port}")
        conn, addr = server.accept()
        with conn:
            data = conn.recv(1024).decode('utf-8')
            print(f"[SERVER-3] Received message from {addr[0]}:{addr[1]}: {data}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', required=True, type=int)
    args = parser.parse_args()
    start_server(args.l)
