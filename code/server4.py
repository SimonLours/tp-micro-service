import socket

serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur.bind(("", 63000))
serveur.listen(1)
print("Serveur prêt...")

conn, addr = serveur.accept()
print(f"Connexion de {addr}")

while True:
    message = conn.recv(1024).decode()
    if message == "fin":
        break
    print("Client dit :", message)
    reponse = input("Répondre > ")
    conn.send(reponse.encode())
    if reponse == "fin":
        break

conn.close()
serveur.close()
