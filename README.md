
# TP - Micro-Service (élément de réseau)

##  PARTIE I – Connexion minimale

**1. À quel moment la socket côté serveur est-elle bloquante ?**  
Quand `accept()` est lancé, le serveur attend un client, donc il bloque. Même chose avec `recv()`, tant qu’il n’y a pas de message, ça attend

**2. Que se passe-t-il si le client se connecte avant que le serveur ne soit prêt ?**  
Il se passe rien ou une erreur “Connection refused” côté client, parce que personne n’écoute encore

**3. Quelle est la différence entre bind() et listen() ?**  
`bind()` réserve l’adresse IP et le port  
`listen()` indique que la socket accepte des connexions

---

##  PARTIE II – Serveur Echo

**1. Pourquoi faut-il une boucle dans le serveur ?**  
Pour qu’il puisse recevoir plusieurs messages sans s’arrêter. Sans boucle, il traite un message et ferme

**2. Que se passe-t-il si on oublie de tester msg == "fin" ?**  
Le serveur tourne en boucle sans fin, même si le client veut partir.

**3. Est-ce que le serveur peut envoyer plusieurs réponses d’affilée ?**  
Non. Il répond une fois à chaque message reçu. Faut changer le code pour autre chose

---

##  PARTIE III – Multi-clients simples

**1. Le serveur peut-il rester actif après une déconnexion client ?**  
Oui. Il revient à `accept()` et attend un nouveau client.

**2. Que faut-il modifier pour accepter plusieurs clients à la suite ?**  
Mettre `accept()` dans une boucle infinie, fermer le client à la fin, recommencer avec un autre

**3. Peut-on imaginer accepter des clients en parallèle ?**  
Oui, avec des threads. Chaque client a son thread à part

---

##  PARTIE IV – Messagerie 1:1

**1. Comment s’assurer que les deux côtés ne parlent pas en même temps ?**  
On fait un tour chacun. Le client parle, le serveur répond, puis le client recommence

**2. Peut-on rendre cet échange non bloquant ? Comment ?**  
Oui. En mode non bloquant avec `setblocking(False)`, `select()`, ou des threads séparés

**3. Quelle est la meilleure façon de quitter proprement la communication ?**  
Envoyer un mot-clé comme “fin”, fermer la socket, sortir de la boucle. C’est propre

---

##  PARTIE V – Calculatrice (eval)

**1. Quels sont les risques d’utiliser eval() ?**  
Ça peut exécuter n’importe quel code, même dangereux. Faut faire très attention

**2. Comment renvoyer une erreur sans faire planter le serveur ?**  
Mettre `eval()` dans un `try/except` et renvoyer l’erreur au client si y’en a une

---

##  PARTIE VI – Mini-protocole

**1. Pourquoi structurer les messages avec /commande ?**  
Pour différencier les commandes du texte normal. C’est clair, simple et facile à gérer.

**2. Comment distinguer facilement les types de messages côté serveur ?**  
On teste si ça commence par `/`, puis on découpe avec `split(" ", 1)` et on traite

---

##  PARTIE VII – Clients en parallèle (threads)

**1. Que se passe-t-il si deux clients envoient des messages en même temps ?**  
S’ils accèdent à la même ressource, ça peut causer des conflits ou des bugs

**2. Peut-on garder un état partagé entre clients ? Est-ce souhaitable ?**  
Oui mais faut un verrou pour protéger. À utiliser que si nécessaire

**3. Que faut-il pour aller plus loin vers une vraie messagerie ?**  
Des pseudos, groupes, historique, messages privés, sécurité, tout un système complet.

---

##  PARTIE VIII – Protection des accès concurrents

**1. Pourquoi faut-il protéger certaines sections du code ?**  
Pour éviter que deux clients écrivent en même temps et foutent le bazar dans les données.

**2. Que risque-t-on si deux clients modifient une même ressource simultanément ?**  
Mélange de messages, pertes de données, crashs. C’est pour ça qu’on met un verrou.

