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

Pour s’assurer que les deux côtés ne parlent pas en même temps, il faut imposer un ordre dans l’échange des messages. Par exemple, on peut décider que :

Le client commence : il envoie un message, puis attend la réponse du serveur.

Le serveur, de son côté, attend de recevoir le message du client, l’affiche, puis saisit sa réponse à envoyer.

Ensuite, le client reprend la main, etc.

Cela crée un dialogue à tour de rôle ("tour par tour"), ce qui évite qu’ils écrivent tous les deux en même temps.

**2. Peut-on rendre cet échange non bloquant ? Comment ?**

Oui, il est possible de rendre l’échange non bloquant.
Pour cela, on peut :

Utiliser le mode non bloquant des sockets (setblocking(False)) : les méthodes recv() ou send() ne bloqueront plus l’exécution, mais il faudra gérer les exceptions si aucune donnée n’est disponible.

Utiliser la fonction select() : cela permet de vérifier si une socket est prête à lire ou écrire avant d’appeler recv() ou send(), évitant ainsi de bloquer le programme.

Ou encore, utiliser des threads : un thread pour écouter les messages entrants, un autre pour gérer l’envoi (mais cela complique la gestion de l’ordre du dialogue).

Mais dans le cadre d’un échange à tour de rôle, le mode bloquant reste plus simple à gérer.

**3. Quelle est la meilleure façon de quitter proprement la communication ?**

La meilleure façon est de :

Prévoir un message spécial (ex : "fin", "quit", etc.) qui indique la volonté de terminer la discussion.

Lorsqu’un des deux participants envoie ce message, les deux programmes doivent alors :

Afficher un message de fermeture,

Fermer proprement la socket avec close(),

Quitter la boucle de dialogue pour terminer le programme sans erreur.

Cela évite les coupures brutales et libère correctement les ressources.


-----------------------------------------------------------------------------------------------------------

-----------------------------------------------------------------------------------------------------------

**__PARTIE V__**

**Quels sont les risques d’utiliser eval() ? (souvenirs de FONDADEV)**

eval() exécute n’importe quelle expression Python passée en argument. Les risques sont donc :

Sécurité : un utilisateur malveillant peut envoyer du code dangereux (ex : os.system("rm -rf /")) et exécuter des commandes sur le serveur.

Stabilité : eval() peut aussi provoquer des exceptions (division par zéro, erreurs de syntaxe…) qui font planter le programme si elles ne sont pas gérées.

Confidentialité : accès possible à des variables ou objets internes du serveur.

Il est donc très dangereux d’utiliser eval() sans contrôle strict.

**2. Comment renvoyer une erreur sans faire planter le serveur ?**

Il faut encapsuler l’appel à eval() dans un bloc try...except pour capturer toute exception :

    try:
    result = eval(expression)  
    conn.send(str(result).encode())
    except Exception as e:
    conn.send(f"Erreur: {e}".encode())
    
-----------------------------------------------------------------------------------------------------------

-----------------------------------------------------------------------------------------------------------

**__PARTIE VI__**

**1.Pourquoi structurer les messages avec /commande ?**

Structurer les messages avec un préfixe (comme /commande) permet de :

Différencier clairement les messages “spéciaux” (commandes) des messages classiques,

Simplifier le traitement côté serveur (ex: /me, /all, /help, etc.),

Rendre le protocole extensible : il suffit d’ajouter de nouvelles commandes,

Faciliter la lecture et la maintenance du code,

Éviter les ambiguïtés dans les échanges (ex : un simple message texte ne sera pas traité comme une commande).


**2.Comment distinguer facilement les types de messages côté serveur ?**

On peut :

Vérifier si un message commence par / pour détecter une commande,

Utiliser la méthode .split(" ", 1) pour séparer le nom de la commande du reste du texte,

Traiter chaque commande avec un if/elif/else ou via un dictionnaire de fonctions associées aux commandes,

Tout message ne commençant pas par / est traité comme un message normal.


-----------------------------------------------------------------------------------------------------------

-----------------------------------------------------------------------------------------------------------

**__PARTIE VII__**

**1.Que se passe-t-il si deux clients envoient des messages en même temps ?**

Si le serveur traite chaque client dans un thread séparé, les deux messages peuvent arriver quasiment en même temps.

Si ces messages doivent accéder à une ressource partagée (par exemple, une liste de messages ou un fichier), il y a un risque de conflit (ex : mélange, écrasement, corruption des données), ce qu’on appelle une condition de course (race condition).

Si chaque client est indépendant et ne p

**2.Peut-on garder un état partagé entre clients ? Est-ce souhaitable ?**

Oui, il est possible de garder un état partagé (ex : une liste commune des messages, ou la liste des utilisateurs connectés).

Mais il faut faire très attention :

Il faut protéger l’accès à cette ressource partagée avec des verrous (mutex, threading.Lock) pour éviter les accès concurrents non contrôlés.

Ce n’est souhaitable que si c’est utile : par exemple, si on veut une messagerie de groupe ou partager des infos entre clients.

Si chaque client doit rester isolé, il vaut mieux éviter le partage.

**3.Que faut-il pour aller plus loin vers une vraie messagerie ?**

Pour s’approcher d’une vraie messagerie :

Gérer les utilisateurs (identifiant, connexion/déconnexion, authentification…),

Gérer la diffusion des messages à plusieurs clients en temps réel,

Maintenir un historique des messages,

Mettre en place un protocole pour les différentes actions (messages privés, groupes, notifications, etc.),

Gérer la concurrence et la robustesse (déconnexions, reconnexions, erreurs),

Sécuriser les échanges (chiffrement, filtrage d’injections, etc.).



-----------------------------------------------------------------------------------------------------------

Pedrero / Lours
