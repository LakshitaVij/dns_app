from flask import Flask, request
import requests
import socket

app = Flask(__name__)

@app.route('/fibonacci')
def get_fibonacci():
    try:
        hostname = request.args.get('hostname')
        fs_port = request.args.get('fs_port')
        number = request.args.get('number')
        as_ip = request.args.get('as_ip')
        as_port = request.args.get('as_port')

        if not all([hostname, fs_port, number, as_ip, as_port]):
            return "400 Bad Request: Missing required parameters", 400

        as_port = int(as_port)

        # Query AS for FS's IP
        dns_query = f"TYPE=A\nNAME={hostname}\n"
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(3)  # Avoids indefinite waiting
        sock.sendto(dns_query.encode(), (as_ip, as_port))

        try:
            response, _ = sock.recvfrom(1024)
        except socket.timeout:
            return "500 Internal Server Error: AS did not respond in time", 500
        finally:
            sock.close()

        response_lines = response.decode().split("\n")

        if not response_lines[0].startswith("VALUE="):
            return "500 Internal Server Error: AS returned an unexpected response", 500

        fs_ip = response_lines[0].split("=")[1]

        if fs_ip == "NOT_FOUND":
            return "500 Internal Server Error: FS is not registered with AS", 500

        # Query FS for Fibonacci number
        fibonacci_url = f"http://{fs_ip}:{fs_port}/fibonacci?number={number}"
        try:
            result = requests.get(fibonacci_url, timeout=5)
            result.raise_for_status()  # Raises an error for HTTP failures
            return result.text, result.status_code
        except requests.exceptions.RequestException as e:
            return f"500 Internal Server Error: Could not connect to FS. Error: {str(e)}", 500

    except Exception as e:
        return f"500 Internal Server Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
