<br>
<p align="center">
    <img src="https://github.com/TheRake66/Pody/blob/main/assets/logo_full.png" alt="logo" width=400>
<p align="center">
Micro-framework de gestion de base de données en Python
<br>
<br>
<a href="https://github.com/TheRake66/Pody/archive/refs/heads/main.zip"><b>• Télécharger •</b></a>
<br>
<br>
<a href="https://github.com/TheRake66/Pody/blob/main/LICENSE"><img alt="GitHub" src="https://img.shields.io/github/license/TheRake66/Pody"></a>
<img alt="Taille du code" src="https://img.shields.io/github/languages/code-size/TheRake66/Pody">
<a href="https://github.com/TheRake66/Pody/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/TheRake66/Pody"></a>
</p>
</p>
<br>



# Pody

Pody est un micro-framework Python destiné à la gestion de base de données en modèle d'objets.
Il permet de manipuler simplement, via des objets, les enregistrements.



## Installation

Pody nécessite python 3 (https://www.python.org/downloads/) ainsi que les modules MySQL suivant :

```
pip3 install mysql
pip3 install mysql-connector-python
```

Faites ensuite un fork de Pody qui servira de base pour votre projet.



## Structure

```
- /Pody
    - /factory
        - /repository
            - converter.py
            - generator.py
            - model.py
            - refection.py
        - clause.py
        - direction.py
        - join.py
        - query.py
    - configuration.py
    - connection.py
- base.py
- pody.py
```

Description des modules :

- converter : Permet de convertir un résultat de requête en modèle.
- generator : Permet de générer les modèles depuis une base de données.
- model : Classe de base parente des modèles implémentant les méthodes CRUD.
- refection : Librairie de réflexion des modèles.
- clause : Énumération des types de clauses.
- direction : Enumeration des types de direction de tri.
- join : Enumeration des types de jointure.
- query : Constructeur de requête SQL.
- configuration : Objet contenant la configuration de connexion de base de données.
- connection : Module gérant les connexions et les interactions avec la base de données.
- base : Template de base d'un projet.
- pody : Outil en ligne de commande pour générer les modèles.



## Utilisation

*Pour les démonstrations, nous utiliserons une base nommée « bdd », qui contient une table nommée « utilisateur », qui contient les champs « id (clé primaire) », « nom », « prenom », « mail ».*


### Connexion à une base de données

Pour se connecter à une base de données il faut dans un premier temps créer la configuration que va avoir celle-ci :

```py
# Nom de la base, nom d'utilisateur, mot de passe, hôte, port
config = Configuration('bdd', 'root', '', 'localhost', 3306)
```

Il faut ensuite ouvrir la connexion :

```py
# Ouverture de la connexion avec la configuration
socket = Connection(config)
```

Quelques exemple de manipulation des connexion :

```py
# Récupération de toutes les connexions
Connection.getAllInstances()

# Récupération de la connexion ayant pour nom de base de données « bdd »
Connection.getInstance('bdd')
```


### Génération des modèles

Maintenant, gênerons les modèles de la base avant leur importation :

```py
# Création du générateur
build = Generator(socket)

# Génération du modèle de la table « utilisateur »
build.generateModels('utilisateur')

# Génération de tous les autres modèles
build.generateModels()

# Importation des modèles
from bdd.utilisateur import Utilisateur
```


### Création des requêtes

Une fois la connexion établie, vous pouvez créer des requêtes comme ceci :

```py
# SELECT nom
# FROM utilisateur
# WHERE id = 3
# AND prenom LIKE '%upon%'

# Via une chaine de caractère
query = Query('''
    SELECT nom
    FROM utilisateur
    WHERE id < 3
    AND prenom LIKE %s
    ''')

# Via les méthodes de construction
query = Query() \
        .select('nom') \
        .from_('utilisateur') \
        .where('id', 3) \
        .and_('prenom', '%s', Clause.LIKE)

# Lancement de la requête sur la connexion a la base de données
socket.runQuery(query, '%upon%')

# Récupération d'une seule ligne
line = socket.fetchOne()

# Conversion de la ligne en objet
user = Converter(Utilisateur).convertWith(line)
```


### Utilisation des méthodes CRUD

Vos êtes prêt a utilisé les méthodes CRUD (Create Read Update Delete), pour cela rien de plus simple, un exemple sur une instance :

```py
# Création d'un utilisateur
Utilisateur(None, 'Dupont', 'Michel', 'm.dupont@gmail.com').create()

# Récupération de l'utilisateur avec l'id « 1 »
user = Utilisateur(1).read()

# Récupération de l'utilisateur avec le nom « Dupont »
user = Utilisateur(None, 'Dupont').read('nom')

# Récupération du premier utilisateur avec l'id au dessus de « 1 »
user = Utilisateur(1).read(None, Clause.GREATER)

# Mise à jour du nom de l'utilisateur
user.nom = 'Marcel'
user.update()

# Suppression de l'utilisateur
user.delete()

# Récupération de tous les utilisateurs ayant une adresse gmail
users = Utilisateur(None, None, None, '%@gmail.com').many('mail', Clause.LIKE)

# Vérifie si l'utilisateur ayant l'id « 2 » existe
Utilisateur(2).exists()

# Compte le nombre d'utilisateurs ayant le nom « Dupont »
Utilisateur(None, 'Dupont').count('nom')
```

Si besoin, on peut également convertir un modèle en JSON :
```py
# Cast de l'utilisateur en string JSON
json = str(user)

# Affichage de l'utilisateur directement en JSON
print(user)
```

Maintenant un exemple de l'une classe de modèle :

```py
# Récupération de tous les utilisateurs
Utilisateur.all()

# Récupération du nombre total d'utilisateur
Utilisateur.size()

# Suppression de tous les utilisateurs
Utilisateur.clear()

# Exécution d'une requête sur la connexion de la base liée à ce modèle
Utilisateur.execute(Query('...'))
```


### Déconnexion de la base de données

Une fois le programme terminé, il faut fermer la connexion :

```py
# Fermeture de la connexion de l'objet « socket »
socket.closeSocket()

# Ferme la connexion de la base de données « bdd »
Connection.closeInstance('bdd')

# Ferme toutes les connexions
Connection.closeAllInstances()
```