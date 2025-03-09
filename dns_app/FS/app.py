from flask import Flask, request
import socket

app = Flask(__name__)

FS_HOSTNAME = "fibonacci.com"
FS_IP = "172.18.0.2"
AS_IP = "10.9.10.2"
AS_PORT = 53533

@app.route('/fibonacci')
def compute_fibonacci():
    number = request.args.get('number')
    if not number or not number.isdigit():
        return "400 Bad Request", 400

    n = int(number)
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b

    return str(a), 200

@app.route('/register', methods=['PUT'])
def register():
    dns_entry = f"TYPE=A\nNAME={FS_HOSTNAME}\nVALUE={FS_IP}\nTTL=10\n"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(dns_entry.encode(), (AS_IP, AS_PORT))
    sock.close()
    return "201 Created", 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)
