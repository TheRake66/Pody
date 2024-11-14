import logging
from time import time

import mysql
import mysql.connector
from mysql.connector.cursor import MySQLCursor
from mysql.connector.connection import MySQLConnection
from mysql.connector import Error

from pody.configuration import Configuration
from pody.factory.query import Query
from pody.factory.repository.converter import Converter



class Connection:
    """Database connection object.
    """
    
    
    __instances: dict = {}
    
    
    @classmethod
    def getAllInstances(cls) -> dict:
        """Returns the list of database connection instances.

        Returns:
            dict:  List of database connection instances.
        """
        return cls.__instances
    
    
    @classmethod
    def getInstance(cls, database: str) -> 'Connection':
        """Returns the database connection instance corresponding to the database name.

        Arguments:
            database (str): Name of the database.

        Returns:
            Connection: Database connection instance.

        Raises:
            Exception: No database connection instance was found.
        """
        if database in cls.__instances:
            return cls.__instances[database]
        else:
            raise Exception(f'No connection to database "{database}" has been established!')


    @classmethod
    def closeAllInstances(cls) -> None:
        """Closes all instances of database connections.
        """
        logging.info('Closing all database connection instances...')
        for instance in cls.__instances.values():
            instance.closeSocket()
        logging.info('All instances have been closed.')
        
    
    @classmethod
    def closeInstance(cls, database: str) -> None:
        """Closes the database connection instance corresponding to the database name.

        Arguments:
            database (str): Name of the database.

        Raises:
            Exception: No database connection instance was found.
        """
        if database in cls.__instances:
            return cls.__instances[database].closeSocket()
        else:
            raise Exception(f'No connection to database "{database}" has been established!')
        
    
    def __init__(self, configuration: Configuration) -> None:
        """Constructor of the class.

        Arguments:
            configuration (Configuration): Database connection configuration object.

        Raises:
            Error: Database connection error.
        """
        try:
            logging.info(f'Connecting to the database "{configuration.getDatabase()}"...')
            self.__configuration = configuration
            self.__connection = mysql.connector.connect(
                host = configuration.getHost(),
                database = configuration.getDatabase(),
                user = configuration.getUser(),
                password = configuration.getPassword(),
                port = configuration.getPort(),
                ssl_disabled = configuration.isUnsecured()
            )
            self.__connection.autocommit = configuration.isAutocommit()
            self.__cursor = self.__connection.cursor(
                dictionary = False,
                prepared = configuration.isPrepared(),
                buffered = configuration.isBuffered()
            )
            self.__instances[configuration.getDatabase()] = self
            logging.info(f'The connection has been established.')
        except Error as error:
            logging.error(f'Unable to connect to the database!')
            logging.error(error)
            raise error
    
    
    def getConfiguration(self) -> Configuration:
        """Returns the database connection configuration object.

        Returns:
            Configuration: Database connection configuration object.
        """
        return self.__configuration
    
    
    def getConnection(self) -> MySQLConnection:
        """Returns the database connection object.

        Returns:
            MySQLConnection: Database connection object.
        """
        return self.__connection
    
    
    def getCursor(self) -> MySQLCursor:
        """Returns the cursor object of the database connection.

        Returns:
            MySQLCursor: Cursor object of the database connection.
        """
        return self.__cursor
    
    
    def getLastInsertId(self) -> int | None:
        """Returns the ID of the last insert.

        Returns:
            int | None: Identifier of the last insertion.
        """
        return self.__cursor.lastrowid
    
    
    def runQuery(self, query: Query, parameters: tuple | str | int | float | bool = ()) -> None:
        """Executes a SQL query.

        Arguments:
            query (Query): Request object.
            parameters (tuple | str | int | float | bool, optional): One or list of query parameters. By default, the list is empty.
        """
        logging.info(f'Executing query "{query}"...')
        if type(parameters) is not tuple:
            parameters = (parameters,)
        config = self.__configuration
        count = len(parameters)
        hastimer = config.hasTimer()
        sql = str(query)
        start, stop = 0, 0
        if count == 0 or type(parameters[0]) is not tuple:
            logging.info(f'Query parameters "{parameters}"...')
            if hastimer: start = time()
            self.__cursor.execute(sql, parameters)
            if hastimer: stop = time()
        else:
            logging.info(f'Multiple execution, parameters not displayable...')
            size = config.getMaxpacket()
            lenght = round(size / len(parameters[0]))
            composites = [ parameters[x:x+lenght] for x in range(0, count, lenght) ]
            if hastimer: start = time()
            for composite in composites:
                self.__cursor.executemany(sql, composite)
            if hastimer: stop = time()
        logging.info(f'Query execution completed.')
        if hastimer:
            seconds = round(stop - start, 3)
            logging.info(f'Query execution time: {seconds} second(s).')
    

    def fetchAll(self) -> list:
        """Retrieves all results of a SQL query.

        Returns:
            list: List of query results.
        """
        rows = self.__cursor.fetchall()
        return [  self.__mergeColumn(row) for row in rows ]
        
        
    def fetchOne(self) -> tuple | None:
        """Retrieves the first result of a SQL query.

        Returns:
            tuple | None: First result of the query.
        """
        row = self.__cursor.fetchone()
        return self.__mergeColumn(row) if not row is None else None
    
    
    def fetchCell(self) -> Any | None:
        """Retrieves the first cell of the first result of a SQL query.

        Returns:
            Any | None: First cell of the first query result.
        """
        row = self.__cursor.fetchone()
        return row[0] if not row is None else None
        
    
    def fetchAllObjects(self, class_: type) -> list:
        """Retrieves all results of a SQL query as a list of objects.

        Arguments:
            class_ (type): Type of object.

        Returns:
            list: List of query results as a list of objects.
        """
        return [ Converter(class_).convertWith(row) for row in self.fetchAll() ]
        
        
    def fetchOneObject(self, class_: type) -> object | None:
        """Retrieves the first result of a SQL query as an object.

        Arguments:
            class_ (type): Type of object.

        Returns:
            object | None: First result of the query as an object.
        """
        row = self.fetchOne()
        return Converter(class_).convertWith(row) if not row is None else None
    
    
    def commitChanges(self) -> None:
        """Manually commits database changes.
        """
        logging.info('Manual commit of changes...')
        self.__connection.commit()
        logging.info('Changes committed.')
        
        
    def rollbackChanges(self) -> None:
        """Manually roll back database changes.
        """
        logging.info('Manually roll back changes...')
        self.__connection.rollback()
        logging.info('Changes roll backed.')
        
        
    def closeSocket(self) -> None:
        """Closes the database connection socket.
        """
        name = self.__configuration.getDatabase()
        logging.info(f'Closing database connection socket "{name}"...')
        self.__cursor.close()
        self.__connection.close()
        self.__instances.pop(name)
        logging.info('Connection socket closed.')
        
        
    def disableForeignKeysChecks(self) -> None:
        """Disables foreign key checks.
        """
        logging.info('Disabling foreign key checks...')
        self.__setForeignKeysChecks(0)
        logging.info('Foreign key checks disabled.')
        
        
    def enableForeignKeysChecks(self) -> None:
        """Enables foreign key checks.
        """
        logging.info('Enabling foreign key checks...')
        self.__setForeignKeysChecks(1)
        logging.info('Foreign key checks enabled.')
    
    
    def __setForeignKeysChecks(self, value: int) -> None:
        """Changes the value of the FOREIGN_KEY_CHECKS variable in MySQL.

        Arguments:
            value (int): New value of the variable.
        """
        query = Query(f'SET FOREIGN_KEY_CHECKS = {value}')
        self.runQuery(query)

    
    def __mergeColumn(self, row: tuple) -> dict:
        """Merges a list of values with column names into a dictionary.

        Returns:
            dict: Merged dictionary.
        """
        return  dict(zip(self.__cursor.column_names, row))