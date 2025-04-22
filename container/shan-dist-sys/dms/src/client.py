import socket
import sys
import argparse

def start_client(host, port):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"[CLIENT] Attempting to connect to {host}:{port}")
        client_socket.connect((host, port))
        print(f"[CLIENT] Successfully connected to {host}:{port}")

        while True:
            try:
                message = input()
                if not message:
                    break
                client_socket.send(message.encode('utf-8'))
            except KeyboardInterrupt:
                break

        client_socket.close()
        print("\n[CLIENT] Connection closed")

    except Exception as e:
        print(f"[CLIENT] Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Message Client')
    parser.add_argument('-c', '--connect', required=True, help='Host:port to connect to')
    args = parser.parse_args()

    try:
        host, port = args.connect.split(':')
        port = int(port)
    except ValueError:
        print("Error: Connection string should be in format host:port")
        sys.exit(1)

    start_client(host, port) 