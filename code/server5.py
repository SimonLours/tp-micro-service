import socket

serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur.bind(("", 63000))
serveur.listen(1)
print("Serveur prêt...")

conn, addr = serveur.accept()
print("Connexion de", addr)

expression = conn.recv(1024).decode()
print("Expression reçue:", expression)

try:
    result = eval(expression)  
    conn.send(str(result).encode())
except Exception as e:
    conn.send(f"Erreur: {e}".encode())

conn.close()
