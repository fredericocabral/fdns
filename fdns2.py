import socket
import socketserver
import ssl


DNSServer = '1.1.1.1'


def upstream_with_tls(data):
    upstream_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Wrap socket with SSL/TLS
    context = ssl.create_default_context()
    tls_sock = context.wrap_socket(upstream_sock, server_hostname=DNSServer)
        
    tls_sock.connect((DNSServer, 853))
    tls_sock.sendall(data)
    received = tls_sock.recv(1024)

    return received


def upstream_without_tls(data):
    upstream_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    upstream_sock.connect((DNSServer, 53))

    upstream_sock.sendall(data)
    received = upstream_sock.recv(1024)

    return received


def upstream_udp(data):
    DNSPort = 53
    
    upstream_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    upstream_sock.sendto(data, (DNSServer, DNSPort))
    received = upstream_sock.recv(1024)

    return received


class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        print('Request receveid')
        #result = upstream(data)
        result = upstream_with_tls(data)
        self.request.sendall(result)


# INPROGRESS
class UDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0]
        socket = self.request[1]
        print("{} wrote:".format(self.client_address[0]))

        epa = upstream_udp(data)

        socket.sendto(data.upper(), self.client_address)


def main():
    port = 9999

    tcp = socketserver.ThreadingTCPServer(('', port), TCPHandler)
    print(f'Listening TCP port {port}')

    #udp = socketserver.ThreadingUDPServer(('', port), UDPHandler)
    #print(f'Listening UDP port {port}')

    #udp.serve_forever()
    tcp.serve_forever()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        tcp.shutdown()

if __name__ == "__main__":
    main()
