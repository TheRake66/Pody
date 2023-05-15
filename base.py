# Import des modules natifs.
import logging

# Import des modules Pody.
from Pody.configuration import Configuration
from Pody.connection import Connection
from Pody.factory.repository.generator import Generator




# Initialisation du logger.
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


# Configuration de la base de données.
config = Configuration('bdd', 'root', '', 'localhost', 3306)

# Connexion à la base de données.
socket = Connection(config)

# Génération des modèles de la base de données.
Generator(socket).generateModels()




# Breakpoint.
pass