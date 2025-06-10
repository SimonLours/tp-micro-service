import socket

serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur.bind(("", 63000))
serveur.listen(1)
print("Serveur prêt, en attente de connexion...")

conn, addr = serveur.accept()
print(f"Connexion de {addr}")

while True:
    msg = conn.recv(1024).decode()
    if msg == "fin":
        print("Fin de la connexion demandée")
        break
    print("Client dit :", msg)
    conn.send(msg.encode())

conn.close()
serveur.close()
