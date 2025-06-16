import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("172.16.20.139", 63000))

print("Tapez /bye pour quitter ou /list pour voir les derniers messages.")

while True:
    msg = input("Vous > ")
    client.send(msg.encode())
    if msg == "/bye":
        break
    reponse = client.recv(2048).decode()
    print("Serveur >", reponse)

client.close()
