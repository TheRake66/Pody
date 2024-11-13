# Import des modules natifs.
import logging

# Import des modules Pody.
from Pody.configuration import Configuration
from Pody.connection import Connection
from Pody.factory.repository.generator import Generator



from test_pody.user import User


# Initialisation du logger.
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


# Configuration de la base de données.
config = Configuration('test_pody', 'root', '', 'localhost', 3306, 65535, True)

# Connexion à la base de données.
socket = Connection(config)

User.clear()


users = []
for i in range(10000):
    users.append(User(i, 'test', 'test', 'test'))
User.inject(users)

print()






# Breakpoint.
pass