import socket

DNS_DB = {}

def handle_request(data, addr, sock):
    lines = data.decode().split("\n")
    if "TYPE=A" in lines[0] and "NAME=" in lines[1]:
        hostname = lines[1].split("=")[1]
        if "VALUE=" in lines[2]:
            DNS_DB[hostname] = lines[2].split("=")[1]
            response = "201 Created\n"
        else:
            response = f"VALUE={DNS_DB.get(hostname, 'NOT_FOUND')}\n"
        sock.sendto(response.encode(), addr)

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", 53533))
    while True:
        data, addr = sock.recvfrom(1024)
        handle_request(data, addr, sock)

if __name__ == "__main__":
    main()
