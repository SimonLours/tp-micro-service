import socket

serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur.bind(("", 63000))
serveur.listen(1)
print("Serveur prêt...")

conn, addr = serveur.accept()
print(f"Connexion de {addr}")

while True:
    expression = conn.recv(1024).decode()
    if expression == "fin":
        break
    print("Expression reçue :", expression)
    try:
        # Eval est risqué, mais ici on l'utilise à titre pédagogique
        result = eval(expression)
        conn.send(str(result).encode())
    except Exception as e:
        conn.send(f"Erreur: {e}".encode())

conn.close()
serveur.close()
