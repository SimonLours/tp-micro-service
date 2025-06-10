import socket

serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur.bind(("", 63000))
serveur.listen(1)
print("Serveur prêt, en attente de connexion...")

conn, addr = serveur.accept()
print(f"Connexion de {addr}")

message = conn.recv(1024).decode()
print("Client dit :", message)

conn.send("Bonjour client !".encode())

conn.close()
serveur.close()
