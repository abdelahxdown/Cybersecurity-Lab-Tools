import socket
import sys

# Petit outil de reconnaissance pour mon labo
# But : Identifier les versions des services pour trouver des failles

def scan_target(ip, ports):
    print(f"[*] Scan de la cible : {ip}")
    for port in ports:
        try:
            s = socket.socket()
            s.settimeout(2)
            s.connect((ip, port))
            # Récupération de la version du service
            banner = s.recv(1024).decode().strip()
            print(f"[+] Port {port} ouvert : {banner}")
            s.close()
        except:
            print(f"[-] Port {port} fermé ou pas de bannière.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scanner_banniere.py <IP>")
        sys.exit()
    
    target = sys.argv[1]
    common_ports = [21, 22, 80, 443]
    scan_target(target, common_ports)
