
from typing import Union



class Configuration:
    """Objet de configuration de la connexion à la base de données.
    """
    
    
    def __init__(self, 
        database : str = 'bdd', 
        user : str = 'root', 
        password : str = '',
        host : str = 'localhost',
        port : int = 3306,
        autocommit : bool = True,
        prepared : bool = True,
        buffered : bool = False,
        maxpacket : int = 65535,
        timer : bool = True,
        beautify : bool = False) -> None:
        """Constructeur de la classe.

        Args:
            database (str, optional): Nom de la base de données. Par défaut 'bdd'.
            user (str, optional): Nom d'utilisateur. Par défaut 'root'.
            password (str, optional): Mot de passe. Vide par défaut.
            host (str, optional): Adresse IP du serveur. Par défaut 'localhost'.
            port (int, optional): Port du serveur. Par défaut 3306.
            autocommit (bool, optional): Activation de l'autocommit. Par défaut True.
            prepared (bool, optional): Activation des requêtes préparées. Par défaut True.
            buffered (bool, optional): Activation de la mise en mémoire tampon. Par défaut False.
            maxpacket (int, optional): Taille maximale des paquets. Par défaut 65535.
            timer (bool, optional): Activation du chronomètre. Par défaut True.
            beautify (bool, optional): Activation de la mise en forme des objets. Par défaut False.
        """
        self.__database = database
        self.__user = user
        self.__password = password
        self.__host = host
        self.__port = port
        self.__autocommit = autocommit
        self.__prepared = prepared
        self.__buffered = buffered
        self.__maxpacket = maxpacket
        self.__timer = timer
        self.__beautify = beautify
        
    
    def getDatabase(self) -> str:
        """Retourne le nom de la base de données.

        Returns:
            str: Nom de la base de données.
        """
        return self.__database
    
    
    def getUser(self) -> str:
        """Retourne le nom d'utilisateur.

        Returns:
            str: Nom d'utilisateur.
        """
        return self.__user
    
    
    def getPassword(self) -> str:
        """Retourne le mot de passe.

        Returns:
            str: Mot de passe.
        """
        return self.__password
    
    
    def getHost(self) -> str:
        """Retourne l'adresse IP du serveur.

        Returns:
            str: Adresse IP du serveur.
        """
        return self.__host
    
    
    def getPort(self) -> int:
        """Retourne le port du serveur.

        Returns:
            int: Port du serveur.
        """
        return self.__port
    
    
    def isAutocommit(self) -> bool:
        """Retourne l'état de l'autocommit.

        Returns:
            bool: État de l'autocommit.
        """
        return self.__autocommit
    
    
    def isPrepared(self) -> bool:
        """Retourne l'état des requêtes préparées.

        Returns:
            bool: État des requêtes préparées.
        """
        return self.__prepared
    
    
    def isBuffered(self) -> bool:
        """Retourne l'état de la mise en mémoire tampon.

        Returns:
            bool: État de la mise en mémoire tampon.
        """
        return self.__buffered
    
    
    def getMaxpacket(self) -> int:
        """Retourne la taille maximale des paquets.

        Returns:
            int: Taille maximale des paquets.
        """
        return self.__maxpacket
    
    
    def hasTimer(self) -> bool:
        """Retourne l'état du chronomètre.

        Returns:
            bool: État du chronomètre.
        """
        return self.__timer
    
    
    def isBeautify(self) -> bool:
        """Retourne l'état de la mise en forme des objets.
        
        Returns:
            bool: État de la mise en forme des objets.
        """
        return self.__beautify