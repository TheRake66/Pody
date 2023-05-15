
import logging
import os
import subprocess

from Pody.configuration import Configuration
from Pody.connection import Connection
from Pody.factory.repository.generator import Generator




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


W  = '\033[0m'  # white (default)
R  = '\033[31m' # red
G  = '\033[32m' # green
Y  = '\033[33m' # yellow
B  = '\033[34m' # blue
P  = '\033[35m' # purple
C  = '\033[36m' # cyan


logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


os.system('cls' if os.name == 'nt' else 'clear')


print(f'''{Y}
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
''')
print(f'''{R}                                                 ░░░▒▒▓▓ Pody ▓▓▒▒░░░''')
print(f'''{Y}                                       ~ Version 1.0.0.0 du 15 septembre 2022 ~''')
print(f'''{Y}                                  ~ Copyright © 2022 - Thibault BUSTOS (TheRake66) ~
      
      
{W}''')


database = ask('Nom de la base de données ("bdd" par défaut) : ', 'bdd')
user = ask('Nom d\'utilisateur ("root" par défaut) : ', 'root')
password = ask('Mot de passe (vide par défaut) : ', '')
host = ask('Adresse IP du serveur ("localhost" par défaut) : ', 'localhost')
port = ask('Port (3306 par défaut) : ', 3306, True)


try:
    config = Configuration(database, user, password, host, port)
    socket = Connection(config)
    
    all = ask('Générer le modèle de toutes les tables ? (O/N) (O par défaut) : ', 'O')
    table = None if all == 'O' or all == 'o' else ask('Nom de la table à générer : ')
        
    try:
        Generator(socket).generateModels(table)
        subprocess.Popen(
            f'explorer /select,"{database}"' if os.name == 'nt' else
            f'open {os.getcwd()}')
    except Exception as e:
        print(f'{R}Erreur lors de la génération des modèles : {e}{W}')
        exit(2)
    
except Exception as e:
    print(f'{R}Erreur lors de la connexion à la base de données : {e}{W}')
    exit(1)

    
    