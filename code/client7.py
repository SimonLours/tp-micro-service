import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("172.16.20.139", 63000))

while True:
    msg = input("Vous > ")
    client.send(msg.encode())
    if msg == "fin":
        break
    reponse = client.recv(1024).decode()
    print("Serveur >", reponse)

client.close()
