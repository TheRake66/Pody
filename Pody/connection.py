import logging
import mysql
import mysql.connector
from typing import List, Dict, Tuple, Union, Optional, Any
from Pody.configuration import Configuration
from Pody.factory.query import Query
from Pody.factory.repository.converter import Converter




class Connection:
    """Objet de connexion à la base de données.
    """
    
    
    __instances = {} # type: dict[str, Connection]
                     # Liste des instances de connexion à la base de données.
    __current = None # type: Connection
                     
                     # Instance courante de connexion à la base de données.
    
    
    @staticmethod
    def getInstances() -> 'dict[str, Connection]':
        """Retourne la liste des instances de connexion à la base de données.

        Returns:
            dict[str, Connection]: Liste des instances de connexion à la base de données.
        """
        return Connection.__instances
    
    
    @staticmethod
    def getInstance(database : str) -> 'Connection':
        """Retourne l'instance de connexion à la base de données correspondant au nom de la base de données.

        Args:
            database (str): Nom de la base de données.

        Raises:
            Exception: Aucune instance de connexion à la base de données n'a été trouvée.

        Returns:
            Connection: Instance de connexion à la base de données.
        """
        if database in Connection.__instances:
            return Connection.__instances[database]
        else:
            raise Exception(f'Aucune connexion à la base de données "{database}" n\'a été établie !')
        
        
    @staticmethod
    def getCurrent() -> 'Connection':
        """Retourne l'instance courante de connexion à la base de données.

        Returns:
            Connection: Instance courante de connexion à la base de données.
        """
        return Connection.__current
    
    
    @staticmethod
    def setCurrent(database : str) -> None:
        """Définit l'instance courante de connexion à la base de données.

        Args:
            database (str): Nom de la base de données.
        """
        Connection.__current = Connection.getInstance(database)
        logging.info(f'Changement de base de données vers "{database}".')
    
    
    def __init__(self, configuration : Configuration) -> None:
        """Constructeur de la classe.

        Args:
            configuration (Configuration): Objet de configuration de la connexion à la base de données.

        Raises:
            error: Erreur de connexion à la base de données.
        """
        self.__configuration = configuration
        try:
            logging.info(f'Connexion à la base de données "{configuration.getDatabase()}"...')
            self.__connection = mysql.connector.connect(
                host = configuration.getHost(),
                database = configuration.getDatabase(),
                user = configuration.getUser(),
                password = configuration.getPassword()
            )
            self.__connection.autocommit = configuration.isAutocommit()
            self.__cursor = self.__connection.cursor(
                prepared = configuration.isPrepared())
            Connection.__instances[configuration.getDatabase()] = self
            Connection.__current = self
        except mysql.connector.Error as error:
            logging.error(f'Impossible de se connecter à la base de données "{configuration.getDatabase()}" !')
            logging.error(error)
            raise error
    
    
    def getConfigurations(self) -> Configuration:
        """Retourne l'objet de configuration de la connexion à la base de données.

        Returns:
            Configuration: Objet de configuration de la connexion à la base de données.
        """
        return self.__configuration
    
    
    def getConnection(self) -> mysql.connector.connection.MySQLConnection:
        """Retourne l'objet de connexion à la base de données.

        Returns:
            mysql.connector.connection.MySQLConnection: Objet de connexion à la base de données.
        """
        return self.__connection
    
    
    def getCursor(self) -> mysql.connector.cursor.MySQLCursor:
        """Retourne l'objet de curseur de la connexion à la base de données.

        Returns:
            mysql.connector.cursor.MySQLCursor: Objet de curseur de la connexion à la base de données.
        """
        return self.__cursor
    
    
    def runQuery(self, query : Query, parameters : tuple = ()) -> 'Connection':
        """Exécute une requête SQL.

        Args:
            query (Query): Objet de requête.
            parameters (tuple, optional): Liste des paramètres de la requête. Par défaut, la liste est vide.
       
        Returns:
            Connection: Instance de connexion à la base de données.
        """
        logging.info(f'Exécution de la requête "{query}"...')
        if not type(parameters) is tuple:
            parameters = (parameters,)
        self.__cursor.execute(str(query), parameters)
        logging.info(f'Exécution de la requête "{query}" terminée.')
        return self
    

    def fetchAll(self) -> List[Union[Tuple, Dict]]:
        """Récupère tous les résultats d'une requête SQL.

        Returns:
            List[Union[Tuple, Dict]]: Liste des résultats de la requête.
        """
        row = self.__cursor.fetchall()
        if self.__configuration.isDictionary():
            return [dict(zip(self.__cursor.column_names, r)) for r in row]
        else:
            return row
        
        
    def fetchOne(self) -> Optional[Union[Tuple, Dict]]:
        """Récupère le premier résultat d'une requête SQL.

        Returns:
            Optional[Union[Tuple, Dict]]: Premier résultat de la requête.
        """
        row = self.__cursor.fetchone()
        if row is None:
            return None
        elif self.__configuration.isDictionary():
            return dict(zip(self.__cursor.column_names, row))
        else:
            return row
        
        
    def fetchOneObject(self, class_ : type) -> Optional[object]:
        """Récupère le premier résultat d'une requête SQL sous forme d'objet.

        Args:
            class_ (type): Type de l'objet.

        Returns:
            Optional[object]: Premier résultat de la requête sous forme d'objet.
        """
        row = self.__cursor.fetchone()
        if row is None:
            return None
        else:
            return Converter(class_).convert(dict(zip(self.__cursor.column_names, row)))
        
    
    def fetchAllObjects(self, class_ : type) -> List[object]:
        """Récupère tous les résultats d'une requête SQL sous forme d'objet.

        Args:
            class_ (type): Type de l'objet.

        Returns:
            List[object]: Liste des résultats de la requête sous forme d'objet.
        """
        return [Converter(class_).convert(dict(zip(self.__cursor.column_names, r))) for r in self.__cursor.fetchall()]
    
    