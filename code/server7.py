import socket
import threading

def gerer_client(conn, addr):
    print(f"[+] Connexion de {addr}")
    while True:
        try:
            msg = conn.recv(1024).decode()
            if not msg or msg == "fin":
                break
            print(f"[{addr}] {msg}")
            conn.send(f"Echo: {msg}".encode())
        except:
            break
    conn.close()
    print(f"[-] Connexion fermée {addr}")

# Création du socket principal
serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur.bind(("", 63000))
serveur.listen()

print("Serveur en écoute sur le port 63000...")

# Boucle infinie pour accepter les connexions
while True:
    conn, addr = serveur.accept()
    thread = threading.Thread(target=gerer_client, args=(conn, addr))
    thread.start()
