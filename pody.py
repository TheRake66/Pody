
import logging
import os
import subprocess

from Pody.configuration import Configuration
from Pody.connection import Connection
from Pody.factory.repository.generator import Generator


os.system('cls' if os.name=='nt' else 'clear')


def ask(text : str, default : any = None, isInt : bool = False) -> str:
    """Demande à l'utilisateur de saisir une valeur.

    Args:
        text (str): Texte à afficher.
        default (any, optional): Valeur par défaut. Par défaut à None.
        isInt (bool, optional): Indique si la valeur saisie doit être un entier. Par défaut à False.

    Returns:
        str: Valeur saisie.
    """
    while True:
        try:
            anwser = input(text).strip()
            if anwser == '':
                anwser = default
            elif isInt:
                anwser = int(anwser)
            return anwser
        except:
            print("Valeur incorrecte !")


W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple
Y = '\033[93m' # yellow


logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


print(f'''{O}
                                   ▄▄▄▄▄▄▄▄▄▄▄                         ▄▄
                                   ████████████▄                       ██
                                   ███ ▄▄▄▄▄▄ ▀██                      ██
                                   ███ ▄▄▄▄▄▄▄ ██▌   ▄▄▄▄▄▄      ▄▄▄▄▄▄██   ▄▄       ▄▄
                                   ███ ▀▀▀▀▀▀▀ ██▌  ████████    █████████  ▐██▌     ▐██▌
                                   ███ ▀▀▀▀▀▀ ▄██  ▐██▀  ▀██▌  ▐██▀  ▀███   ▐██▌   ▐██▌
                                   ████████████▀   ██▌    ▐██  ██▌    ▐██    ▐██▌ ▐██▌
                                   ███▀▀▀▀▀▀▀▀     ▐██▄  ▄██▌  ▐██▄  ▄██▌     ▐██▄██▌
                                   ███              ████████    ████████       ▐███▌
                                   ███               ▀▀▀▀▀▀      ▀▀▀▀▀▀        ███▀
                                                                              ███
                                                                             ███
                                                                           ▄███
                                                                           ▀▀▀
{W}''')
print(f'''{R}                                                 ░░░▒▒▓▓ Pody ▓▓▒▒░░░{W}''')
print(f'''{Y}                                       ~ Version 1.0.0.0 du 15 septembre 2022 ~{W}''')
print(f'''{Y}                                  ~ Copyright © 2022 - Thibault BUSTOS (TheRake66) ~
      
      
{W}''')


database = ask('Nom de la base de données ("test" par défaut) : ', 'test')
user = ask('Nom d\'utilisateur ("root" par défaut) : ', 'root')
password = ask('Mot de passe (vide par défaut) : ', '')
host = ask('Adresse IP du serveur ("localhost" par défaut) : ', 'localhost')
port = ask('Port (3306 par défaut) : ', 3306, True)


try:
    logging.info('Connexion à la base de données...')
    config = Configuration(database, user, password, host, port)
    Connection(config)
    logging.info('Connexion établie !')
except Exception as e:
    logging.error(f'Erreur lors de la connexion à la base de données : {e}')
    exit(1)


all = ask('Générer le modèle de toutes les tables ? (O/N) (O par défaut) : ', 'O')
table = None if all == 'O' or all == 'o' else ask('Nom de la table à générer : ')
    
    
try:
    logging.info('Génération du modèle...')
    Generator().generate(table)
    logging.info('Modèle généré !') 
    subprocess.Popen(f'explorer /select,"{database}"')
except Exception as e:
    logging.error(f'Erreur lors de la génération du modèle : {e}')
    exit(1)

    
    
