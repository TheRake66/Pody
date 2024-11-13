


class Configuration:
    """Database connection configuration object.

    Attributes:
        database (str, optional): Database name. Default is 'db'.
        user (str, optional): Username. Default is 'root'.
        password (str, optional): Password. Empty by default.
        host (str, optional): Server IP address. Default is 'localhost'.
        port (int, optional): Server port. Default 3306.
        maxpacket (int, optional): Maximum packet size. Default 65535.
        unsecured (bool, optional): Disable SSL protocol. Default is False.
        autocommit (bool, optional): Enable autocommit. Default is True.
        prepared (bool, optional): Enable prepared statements. Default is True.
        buffered (bool, optional): Enable buffering. Default is False.
        timer (bool, optional): Enable timer. Default is True.
        beautify (bool, optional): Enable object formatting. Default is False.
    """
    
    
    def __init__(self, 
        database: str = 'db', 
        user: str = 'root', 
        password: str = '',
        host: str = 'localhost',
        port: int = 3306,
        maxpacket: int = 65535,
        unsecured: bool = False,
        autocommit: bool = True,
        prepared: bool = True,
        buffered: bool = False,
        timer: bool = True,
        beautify: bool = False) -> None:
        """Constructor of the class.

        Arguments:
            database (str, optional): Database name. Default is 'db'.
            user (str, optional): Username. Default is 'root'.
            password (str, optional): Password. Empty by default.
            host (str, optional): Server IP address. Default is 'localhost'.
            port (int, optional): Server port. Default 3306.
            maxpacket (int, optional): Maximum packet size. Default 65535.
            unsecured (bool, optional): Disable SSL protocol. Default is False.
            autocommit (bool, optional): Enable autocommit. Default is True.
            prepared (bool, optional): Enable prepared statements. Default is True.
            buffered (bool, optional): Enable buffering. Default is False.
            timer (bool, optional): Enable timer. Default is True.
            beautify (bool, optional): Enable object formatting. Default is False.
        """
        self.__database = database
        self.__user = user
        self.__password = password
        self.__host = host
        self.__port = port
        self.__maxpacket = maxpacket
        self.__unsecured = unsecured
        self.__autocommit = autocommit
        self.__prepared = prepared
        self.__buffered = buffered
        self.__timer = timer
        self.__beautify = beautify
        
    
    def getDatabase(self) -> str:
        """Return database name.

        Returns:
            str: Database name.
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
    
    
    def getMaxpacket(self) -> int:
        """Retourne la taille maximale des paquets.

        Returns:
            int: Taille maximale des paquets.
        """
        return self.__maxpacket
    
    
    def isUnsecured(self) -> bool:
        """Retourne l'état du protocole SSL.

        Returns:
            bool: État du protocole SSL.
        """
        return self.__unsecured
    
    
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