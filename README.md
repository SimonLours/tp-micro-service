# tp-micro-service


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






Pedrero / Lours
