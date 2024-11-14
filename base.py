# Import des modules natifs.
import logging

# Import des modules Pody.
from pody.configuration import Configuration
from pody.connection import Connection
from pody.factory.query import Query
from pody.factory.repository.generator import Generator



from test_pody.user import User


# Initialisation du logger.
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


# Configuration de la base de données.
config = Configuration('test_pody', 'root', '', 'localhost', 3306, 65535, True)

# Connexion à la base de données.
socket = Connection(config)




#for i in range(1, 10):
#    User(i, f'test{i}', f'test{i}', f'test{i}@gmai.com').create()


a = socket.runQuery(Query('select name from user where id = 1222323')).fetchOne()




socket.closeSocket()



# Breakpoint.
pass