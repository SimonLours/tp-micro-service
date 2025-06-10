import socket

serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur.bind(("", 63000))
serveur.listen(1)
print("Serveur prêt, en écoute...")

while True:
    conn, addr = serveur.accept()
    print(f"Connexion de {addr}")

    while True:
        msg = conn.recv(1024).decode()
        if msg == "fin":
            print(f"Fin de connexion avec {addr}")
            break
        print(f"Client {addr} dit : {msg}")
        conn.send(msg.encode())

    conn.close()
