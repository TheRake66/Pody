


class Configuration:
    """Database connection configuration object.
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
        """Return username.

        Returns:
            str: Username.
        """
        return self.__user
    
    
    def getPassword(self) -> str:
        """Return password.

        Returns:
            str: password.
        """
        return self.__password
    
    
    def getHost(self) -> str:
        """Return server IP address.

        Returns:
            str: Server IP address.
        """
        return self.__host
    
    
    def getPort(self) -> int:
        """Return server port.
 
        Returns:
            str: Server port.
        """
        return self.__port
    
    
    def getMaxpacket(self) -> int:
        """Return maximum packet size.

        Returns:
            int: Maximum packet size.
        """
        return self.__maxpacket
    
    
    def isUnsecured(self) -> bool:
        """Return if SSL protocol is disabled.

        Returns:
            bool: If SSL protocol is disabled.
        """
        return self.__unsecured
    
    
    def isAutocommit(self) -> bool:
        """Retourne if autocommit is enabled.

        Returns:
            bool: If autocommit is enabled.
        """
        return self.__autocommit
    
    
    def isPrepared(self) -> bool:
        """Retourne if prepared statements is enabled.

        Returns:
            bool: If prepared statements is enabled.
        """
        return self.__prepared
    
    
    def isBuffered(self) -> bool:
        """Retourne if buffering is enabled.

        Returns:
            bool: If buffering is enabled.
        """
        return self.__buffered
    
    
    def hasTimer(self) -> bool:
        """Retourne if has a timer.

        Returns:
            bool: If has a timer.
        """
        return self.__timer
    
    
    def isBeautify(self) -> bool:
        """Retourne if object formatting is enabled.

        Returns:
            bool: If object formatting is enabled.
        """
        return self.__beautify