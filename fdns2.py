import os
import socket
import socketserver
import ssl
import threading

CLOUDFLARE = '1.1.1.1'
DNSSERVER = os.getenv('DNSSERVER', CLOUDFLARE)

PORT = 9999
HOST = ''


def upstream_with_tls(data):
    upstream_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Wrap socket with SSL/TLS
    context = ssl.create_default_context()
    tls_sock = context.wrap_socket(upstream_sock, server_hostname=DNSSERVER)
        
    tls_sock.connect((DNSSERVER, 853))
    tls_sock.sendall(data)
    return tls_sock.recv(1024)


class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        print('TCP request receveid')
        result = upstream_with_tls(data)
        self.request.sendall(result)


#def convert(data):
#    pre_length = "\x00"+chr(len(data))
#    data = pre_length + data
#    return _query


# PENDING
class UDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print(self.request)
        data = self.request[0].strip()
        socket = self.request[1]
        print('UDP request receveid')
        result = upstream_without_tls(data)
        socket.sendto(result, self.client_address)


def main():
    tcp = socketserver.ThreadingTCPServer((HOST, PORT), TCPHandler)
    tcp_thread = threading.Thread(target=tcp.serve_forever())
    tcp_thread.daemon = True
    tcp_thread.start()

    #udp = socketserver.ThreadingUDPServer((HOST, PORT), UDPHandler)
    #udp_thread = threading.Thread(target=udp.serve_forever())
    #udp_thread.daemon = True
    #udp_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        tcp.shutdown()

if __name__ == "__main__":
    print('starting fdns')
    print(f'UPSTREAM DNS: {DNSSERVER}')
    main()
