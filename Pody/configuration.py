
class Configuration:
    """Objet de configuration de la connexion à la base de données.
    """
    
    
    def __init__(self, 
                database : str = 'test', 
                user : str = 'root', 
                password : str = '',
                host : str = 'localhost',
                port : int = 3306,
                autocommit : bool = False,
                prepared : bool = True,
                dictionary : bool = True) -> None:
        """Constructeur de la classe.

        Args:
            database (str, optional): Nom de la base de données. Par défaut '***REMOVED***'.
            user (str, optional): Nom d'utilisateur. Par défaut '***REMOVED***'.
            password (str, optional): Mot de passe. Par défaut '***REMOVED***'.
            host (str, optional): Adresse IP du serveur. Par défaut '***REMOVED***'.
            port (int, optional): Port du serveur. Par défaut ***REMOVED***.
            autocommit (bool, optional): Activation de l'autocommit. Par défaut False.
            prepared (bool, optional): Activation des requêtes préparées. Par défaut True.
            dictionary (bool, optional): Activation du dictionnaire. Par défaut True.
        """
        self.__database = database
        self.__user = user
        self.__password = password
        self.__host = host
        self.__port = port
        self.__autocommit = autocommit
        self.__prepared = prepared
        self.__dictionary = dictionary
        
    
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
            bool: Activation de l'autocommit.
        """
        return self.__autocommit
    
    
    def isPrepared(self) -> bool:
        """Retourne l'état des requêtes préparées.

        Returns:
            bool: Activation des requêtes préparées.
        """
        return self.__prepared
    
    
    def isDictionary(self) -> bool:
        """Retourne l'état du dictionnaire.

        Returns:
            bool: Activation du dictionnaire.
        """
        return self.__dictionary