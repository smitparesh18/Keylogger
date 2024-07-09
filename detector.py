import os
import psutil
import socket

# List of known keylogger processes and file names (example list)
known_keyloggers = [
    "keylogger.py",
    "kl.exe",
    "logkeys",
    
]

# Directories to scan for suspicious files
scan_directories = [
    "C:\\Windows\\System32",
    "C:\\Windows",
    "C:\\Users\\Public",
    "C:\\Users\\<YourUsername>\\AppData\\Roaming",
    "C:\\Users\\<YourUsername>\\AppData\\Local",
]

# Function to check for suspicious processes
def check_processes():
    suspicious_processes = []
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        try:
            process_name = proc.info['name']
            if process_name.lower() in known_keyloggers:
                suspicious_processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return suspicious_processes

# Function to scan directories for suspicious files
def scan_files():
    suspicious_files = []
    for directory in scan_directories:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.lower() in known_keyloggers:
                    suspicious_files.append(os.path.join(root, file))
    return suspicious_files

# Function to check for suspicious network activity
def check_network_activity():
    suspicious_networks = []
    connections = psutil.net_connections(kind='inet')
    for conn in connections:
        if conn.status == psutil.CONN_ESTABLISHED:
            try:
                remote_ip = conn.raddr.ip
                remote_host = socket.gethostbyaddr(remote_ip)
                if remote_host:
                    suspicious_networks.append((remote_ip, remote_host))
            except (socket.herror, socket.gaierror):
                pass
    return suspicious_networks

def main():
    print("Checking for suspicious processes...")
    suspicious_processes = check_processes()
    if suspicious_processes:
        print("Suspicious processes found:")
        for proc in suspicious_processes:
            print(proc)
    else:
        print("No suspicious processes found.")

    print("\nScanning for suspicious files...")
    suspicious_files = scan_files()
    if suspicious_files:
        print("Suspicious files found:")
        for file in suspicious_files:
            print(file)
    else:
        print("No suspicious files found.")

   

if __name__ == "__main__":
    main()
