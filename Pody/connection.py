import logging
from time import time
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
    
    
    @classmethod
    def getAllInstances(cls) -> 'dict[str, Connection]':
        """Retourne la liste des instances de connexion à la base de données.

        Returns:
            dict[str, Connection]: Liste des instances de connexion à la base de données.
        """
        return cls.__instances
    
    
    @classmethod
    def getInstance(cls, database : str) -> 'Connection':
        """Retourne l'instance de connexion à la base de données correspondant au nom de la base de données.

        Args:
            database (str): Nom de la base de données.

        Raises:
            Exception: Aucune instance de connexion à la base de données n'a été trouvée.

        Returns:
            Connection: Instance de connexion à la base de données.
        """
        if database in cls.__instances:
            return cls.__instances[database]
        else:
            raise Exception(f'Aucune connexion à la base de données "{database}" n\'a été établie !')


    @classmethod
    def closeAllInstances(cls) -> None:
        """Ferme toutes les instances de connexion à la base de données.
        """
        logging.info('Fermeture de toutes les instances de connexion à la base de données...')
        for instance in cls.__instances.values():
            instance.closeSocket()
        logging.info('Toutes les instances ont été fermées.')
        
    
    @classmethod
    def closeInstance(cls, database : str) -> None:
        """Ferme l'instance de connexion à la base de données correspondant au nom de la base de données.

        Args:
            database (str): Nom de la base de données.
        """
        if database in cls.__instances:
            return cls.__instances[database].closeSocket()
        else:
            raise Exception(f'Aucune connexion à la base de données "{database}" n\'a été établie !')
        
    
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
                password = configuration.getPassword(),
                port = configuration.getPort()
            )
            self.__connection.autocommit = configuration.isAutocommit()
            self.__cursor = self.__connection.cursor(
                dictionary = False,
                prepared = configuration.isPrepared(),
                buffered = configuration.isBuffered())
            self.__instances[configuration.getDatabase()] = self
            logging.info(f'La connexion a été établie.')
        except mysql.connector.Error as error:
            logging.error(f'Impossible de se connecter !')
            logging.error(error)
            raise error
    
    
    def getConfiguration(self) -> Configuration:
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
    
    
    def getLastInsertId(self) -> int:
        """Retourne l'identifiant de la dernière insertion.

        Returns:
            int: Identifiant de la dernière insertion.
        """
        return self.__cursor.lastrowid
    
    
    def runQuery(self, query : Query, parameters : Union[tuple, Any] = ()) -> 'Connection':
        """Exécute une requête SQL.

        Args:
            query (Query): Objet de requête.
            parameters  (Union[tuple, Any], optional): Liste des paramètres de la requête. Par défaut, la liste est vide.
       
        Returns:
            Connection: Instance de connexion à la base de données.
        """
        logging.info(f'Exécution de la requête "{query}"...')
        if type(parameters) is not tuple:
            parameters = (parameters,)
        config = self.getConfiguration()
        count = len(parameters)
        hastimer = config.hasTimer()
        sql = str(query)
        start, stop = 0, 0
        if count == 0 or type(parameters[0]) is not tuple:
            logging.info(f'Paramètres de la requête "{parameters}"...')
            if hastimer: start = time()
            self.__cursor.execute(sql, parameters)
            if hastimer: stop = time()
        else:
            logging.info(f'Exécution multiple, paramètres non affichables...')
            size = config.getMaxpacket()
            lenght = round(size / len(parameters[0]))
            composites = [ parameters[x:x+lenght] for x in range(0, count, lenght) ]
            if hastimer: start = time()
            for composite in composites:
                self.__cursor.executemany(sql, composite)
            if hastimer: stop = time()
        logging.info(f'Exécution de la requête terminée.')
        if hastimer:
            seconds = round(stop - start, 3)
            logging.info(f'Temps d\'exécution de la requête : {seconds} secondes.')
        return self
    

    def fetchAll(self) -> List[Union[Tuple, Dict]]:
        """Récupère tous les résultats d'une requête SQL.

        Returns:
            List[Union[Tuple, Dict]]: Liste des résultats de la requête.
        """
        return [ dict(zip(self.__cursor.column_names, r)) for r in self.__cursor.fetchall() ]
        
        
    def fetchOne(self) -> Optional[Union[Tuple, Dict]]:
        """Récupère le premier résultat d'une requête SQL.

        Returns:
            Optional[Union[Tuple, Dict]]: Premier résultat de la requête.
        """
        row = self.__cursor.fetchone()
        return dict(zip(self.__cursor.column_names, row)) if not row is None else None
    
    
    def fetchCell(self) -> Optional[Union[Tuple, Dict]]:
        """Récupère la première cellule du premier résultat d'une requête SQL.

        Returns:
            Optional[Union[Tuple, Dict]]: Première cellule du premier résultat de la requête.
        """
        row = self.__cursor.fetchone()
        return row[0] if not row is None else None
        
    
    def fetchAllObjects(self, class_ : type) -> List[object]:
        """Récupère tous les résultats d'une requête SQL sous forme d'objet.

        Args:
            class_ (type): Type de l'objet.

        Returns:
            List[object]: Liste des résultats de la requête sous forme d'objet.
        """
        return [ Converter(class_).convertWith(row) for row in self.fetchAll() ]
        
        
    def fetchOneObject(self, class_ : type) -> Optional[object]:
        """Récupère le premier résultat d'une requête SQL sous forme d'objet.

        Args:
            class_ (type): Type de l'objet.

        Returns:
            Optional[object]: Premier résultat de la requête sous forme d'objet.
        """
        row = self.fetchOne()
        return Converter(class_).convertWith(row) if not row is None else None
    
    
    def commitChanges(self) -> None:
        """Valide manuellement les modifications de la base de données.
        """
        logging.info('Validation manuelle des modifications...')
        self.__connection.commit()
        logging.info('Modifications validées.')
        
        
    def rollbackChanges(self) -> None:
        """Annule manuellement les modifications de la base de données.
        """
        logging.info('Annulation manuelle des modifications...')
        self.__connection.rollback()
        logging.info('Modifications annulées.')
        
        
    def closeSocket(self) -> None:
        """Ferme le socket de connexion à la base de données.
        """
        logging.info(f'Fermeture du socket de connexion de la base de données "{self.__configuration.getDatabase()}"...')
        self.__cursor.close()
        self.__connection.close()
        self.__instances.pop(self.__configuration.getDatabase())
        logging.info('Socket de connexion fermé.')
        
        
    def disableForeignKeysChecks(self) -> None:
        """Désactive les contrôles de clés étrangères.
        """
        logging.info('Désactivation des contrôles de clés étrangères...')
        query = Query('SET FOREIGN_KEY_CHECKS = 0')
        self.runQuery(query)
        logging.info('Contrôles de clés étrangères désactivés.')
        
        
    def enableForeignKeysChecks(self) -> None:
        """Active les contrôles de clés étrangères.
        """
        logging.info('Activation des contrôles de clés étrangères...')
        query = Query('SET FOREIGN_KEY_CHECKS = 1')
        self.runQuery(query)
        logging.info('Contrôles de clés étrangères activés.')