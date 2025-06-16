import socket

serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur.bind(("", 63000))
serveur.listen(1)
print("Serveur prêt pour des calculs...")

conn, addr = serveur.accept()
print(f"Client connecté depuis {addr}")

while True:
    expression = conn.recv(1024).decode()
    if expression.lower() == "fin":
        break

    print("Expression reçue :", expression)

    try:
        # Attention : eval() exécute du code Python, dangereux en prod !
        result = eval(expression)
        conn.send(str(result).encode())
    except Exception as e:
        conn.send(f"Erreur: {e}".encode())

conn.close()
serveur.close()
