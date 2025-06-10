# __tp-micro-service__

-----------------------------------------------------------------------------------------------------------

-----------------------------------------------------------------------------------------------------------

**__PARTIE I__**


**1. À quel moment la socket côté serveur est-elle bloquante ?**

La socket côté serveur devient bloquante lors de l’appel à la méthode accept().
En effet, quand le serveur exécute la ligne conn, addr = serveur.accept(), il attend (bloque) qu’un client se connecte. Tant qu’aucun client ne tente de connexion, cette ligne reste bloquée et le programme serveur ne continue pas plus loin.

D’autres appels, comme recv() (lecture de données sur la socket), sont également bloquants par défaut : ils attendent l’arrivée de données.
On dit que le serveur est “bloqué” dans ces appels car il attend un événement extérieur (connexion ou message du client), et rien ne se passe tant que cet événement n’arrive pas


**2. Que se passe-t-il si le client se connecte avant que le serveur ne soit prêt ?**

Si le client tente de se connecter avant que le serveur n’ait appelé bind() et listen(), la connexion échoue.
Dans ce cas, le client reçoit une erreur du type “Connection refused” (connexion refusée), car il n’y a rien qui écoute sur le port demandé.
Le client doit donc être lancé après le serveur pour que la connexion puisse s’établir correctement


**3. Quelle est la différence entre bind() et listen() ?**

bind() : permet d’associer la socket à une adresse IP et à un port sur la machine.
→ C’est comme “réserver” une porte d’entrée sur l’ordinateur pour écouter les connexions à venir.

listen() : indique que la socket est maintenant prête à accepter des connexions entrantes.
→ C’est le moment où le serveur “ouvre la porte” et se met en attente des demandes de connexion.


-----------------------------------------------------------------------------------------------------------

-----------------------------------------------------------------------------------------------------------

**__PARTIE II__**

**1. Pourquoi faut-il une boucle dans le serveur ?**

Il faut une boucle dans le serveur pour pouvoir gérer plusieurs messages successifs envoyés par le client, sans avoir à recréer la connexion à chaque fois.
La boucle permet d’écouter continuellement les messages, de les traiter (ici : les renvoyer, effet “echo”) tant que la communication n’est pas terminée.
Sans boucle, le serveur traiterait un seul message puis s’arrêterait, ce qui limiterait énormément l’intérêt d’une communication réseau.

**2. Que se passe-t-il si on oublie de tester msg == "fin" ?**

Si on oublie de tester msg == "fin", la boucle ne s’arrêtera jamais automatiquement, même quand le client souhaite mettre fin à la communication.
Le serveur restera bloqué à attendre et traiter les messages indéfiniment, ou continuera à renvoyer les mêmes messages sans jamais fermer la connexion.
Cela peut provoquer un blocage ou forcer le client à fermer brutalement la connexion, ce qui n’est pas propre.

**3. Est-ce que le serveur peut envoyer plusieurs réponses d’affilée ?**

Non, le serveur Echo classique n’envoie une réponse qu’après avoir reçu un message du client (il fait un “echo” : un message reçu = un message renvoyé).
Pour envoyer plusieurs réponses d’affilée, il faudrait modifier le code pour envoyer plusieurs messages depuis le serveur sans attendre une demande du client.
Dans le modèle “echo”, chaque message du client entraîne une seule réponse immédiate du serveur, pas plus.


-----------------------------------------------------------------------------------------------------------

-----------------------------------------------------------------------------------------------------------

**__PARTIE III__**

**1. Le serveur peut-il rester actif après une déconnexion client ?**

Oui, le serveur peut parfaitement rester actif après la déconnexion d’un client.
Il suffit d’utiliser une boucle principale qui relance l’attente d’une nouvelle connexion (serveur.accept()) chaque fois qu’un client termine la communication et que sa socket est fermée.
Ainsi, le serveur est capable d’enchaîner les connexions successives sans s’arrêter, il reste donc en fonctionnement en attendant d’autres clients.

**2. Que faut-il modifier pour accepter plusieurs clients à la suite ?**

Pour accepter plusieurs clients à la suite, il faut :

Mettre l’appel à accept() dans une boucle infinie (par exemple, while True:).

À chaque nouvelle connexion (conn, addr = serveur.accept()), gérer la communication avec ce client, puis fermer la socket correspondante une fois la communication terminée.

Ensuite, la boucle recommence et le serveur est prêt à accepter un nouveau client.

Cela permet d’enchaîner les clients un par un, sans avoir besoin de relancer le serveur à chaque fois.

**3. Peut-on imaginer accepter des clients en parallèle ?**

Oui, il est tout à fait possible d’accepter des clients en parallèle.
Pour cela, on utilise par exemple des threads

-----------------------------------------------------------------------------------------------------------

-----------------------------------------------------------------------------------------------------------

**__PARTIE IV__**

**1. Comment s’assurer que les deux côtés ne parlent pas en même temps ?**

Pour s’assurer que les deux côtés ne parlent pas en même temps, il faut instaurer un tour de parole :

Soit en définissant une règle stricte dans le protocole (par exemple, le client écrit, puis le serveur répond, et ainsi de suite).

Soit en alternant systématiquement l’envoi et la réception (chacun attend son tour pour envoyer un message).

**2. Peut-on rendre cet échange non bloquant ? Comment ?**

Oui, on peut rendre l’échange non bloquant :

En utilisant des threads (un pour envoyer, un pour recevoir), chaque côté peut écouter et parler indépendamment.

Ou en utilisant la fonction select() (ou des sockets en mode non bloquant), qui permet de savoir si des données sont prêtes à être lues ou écrites sans bloquer le programme.

**3. Quelle est la meilleure façon de quitter proprement la communication ?**

La meilleure façon de quitter proprement la communication est de :

Envoyer un message spécial (par exemple, "fin", /quit, etc.) pour prévenir l’autre côté de la fermeture.

Ensuite, chaque côté peut fermer la socket de manière propre avec la méthode .close(), ce qui libère les ressources réseau.

-----------------------------------------------------------------------------------------------------------

Pedrero / Lours
