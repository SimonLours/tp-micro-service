import socket
import threading

messages = []              # Liste partagée des messages
lock = threading.Lock()    # Verrou pr protéger la ressource partagée

def gerer_client(conn, addr):
    pseudo = f"{addr[0]}:{addr[1]}"
    print(f"[+] Connexion de {pseudo}")

    while True:
        try:
            msg = conn.recv(1024).decode()
            if not msg or msg == "/bye":
                break

            if msg.startswith("/list"):
                with lock:
                    historique = "\n".join(messages[-10:]) or "Aucun message pour l'instant."
                conn.send(historique.encode())

            else:
                with lock:
                    messages.append(f"[{pseudo}] {msg}")
                print(f"[{pseudo}] {msg}")
                conn.send("Message reçu et stocké.".encode())

        except Exception as e:
            print(f"[!] Erreur avec {pseudo} :", e)
            break

    conn.close()
    print(f"[-] Connexion fermée {pseudo}")

serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur.bind(("", 63000))
serveur.listen()
print("🟢 Serveur prêt (accès concurrent protégé + historique avec /list)")

while True:
    conn, addr = serveur.accept()
    thread = threading.Thread(target=gerer_client, args=(conn, addr))
    thread.start()
