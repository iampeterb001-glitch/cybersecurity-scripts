import socket
import sys

def scan_ports(host, start_port, end_port):
    print(f"Scanning {host} from port {start_port} to {end_port}...")
    open_ports = []
    
    for port in range(start_port, end_port + 1):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            if result == 0:
                open_ports.append(port)
                print(f"Port {port} is OPEN")
            sock.close()
        except socket.gaierror:
            print(f"Hostname {host} could not be resolved")
            break
    
    print(f"\nScan complete. Open ports: {open_ports}")

if __name__ == "__main__":
    host = input("Enter target IP or hostname: ")
    start = int(input("Enter start port (default 1): ") or "1")
    end = int(input("Enter end port (default 1024): ") or "1024")
    scan_ports(host, start, end)