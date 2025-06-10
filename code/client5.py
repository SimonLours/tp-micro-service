import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("172.16.20.139", 63000))

while True:
    expr = input("Entrez une expression à calculer : ")
    client.send(expr.encode())
    if expr == "fin":
        break
    result = client.recv(1024).decode()
    print("Résultat :", result)

client.close()
