import ipaddress
import os
import platform
import subprocess

def is_admin():
    try:
        return os.getuid() == 0
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0

def get_network_from_gateway(default_gateway):
    network = ipaddress.ip_network(default_gateway + "/24", strict=False)
    return network

def ping_ip(ip):
    if platform.system().lower() == "windows":
        command = ["ping", "-n", "1", "-w", "1000", str(ip)]
    else:
        command = ["ping", "-c", "1", "-W", "1", str(ip)]
    
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode == 0

def scan_network(network):
    active_ips = set()
    for ip in network.hosts():
        if ping_ip(ip):
            active_ips.add(ip)
    return active_ips

def find_unused_ips(network, active_ips):
    unused_ips = [str(ip) for ip in network.hosts() if ip not in active_ips]
    return unused_ips

def save_to_file(unused_ips, filename="unused_ips.txt"):
    with open(filename, "w") as file:
        for ip in unused_ips:
            file.write(ip + "\n")

def main():
    if not is_admin():
        print("This script must be run as an administrator.")
        return
    
    default_gateway = input("Enter the default gateway (e.g. 192.168.1.1): ")
    try:
        network = get_network_from_gateway(default_gateway)
        active_ips = scan_network(network)
        unused_ips = find_unused_ips(network, active_ips)
        save_to_file(unused_ips)
        print(f"Unused IPs have been saved to {os.path.abspath('unused_ips.txt')}")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import ctypes
    main()
