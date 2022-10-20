import os
import sys
import socket

def singlePort():
    print(f"\n------------------- Scaning {ipAlvo} -------------------\n")
    setPorts = [21, 22, 23, 80, 81, 110, 139, 443, 445, 465, 1433, 3389, 3390, 5038, 5555, 5900, 8080, 8291, 8545]
    for ports in setPorts:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.3)

        if s.connect_ex((ipAlvo, ports)) == 0:
            print(f"Port {ports} open!")
            print(f"{ipAlvo},{ports}", file=arquivo)
            s.close()
                
        else:
            print(f"Port {ports} close!")
            s.close()

ipAlvo = sys.argv[1]
path = sys.argv[2]
with open(f"{path}open_ports_{ipAlvo}.txt", 'w') as arquivo:
    singlePort()

