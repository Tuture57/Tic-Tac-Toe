import socket


## HOST = "10.214.208.74"
PORT = 1023


# créer l'objet socket
s = socket.socket()

# Ne pas mettre d'ip permet de le mettre en mode détection pour les autres ip du réseau
s.bind(("", PORT))
print("le serveur tourne sur le port", PORT)

#active le mode détection
s.listen(3)
print("La detection d'autres appareils et active")

# boucle infinie pour ne pas stopper la connexion sauf erreur
while True:

# connect ca va créer l'objet utilisable pour envoyer et recevoir et addr va etre l'adresse associé au client
    connec, addr = s.accept()
    print("Connexion etablie avec", addr)

    connec.send("test".encode())

