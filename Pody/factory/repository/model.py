import logging
from typing import Union

from Pody.connection import Connection
from Pody.factory.clause import Clause
from Pody.factory.query import Query
from Pody.factory.repository.reflection import Reflection


class Model:
    """Gestion des méthodes liées au modèle de données.
    """
    
    
    @classmethod
    def all(cls) -> list:
        """Récupération de tous les modèles de la base de données.

        Returns:
            list: La liste des objets modèles.
        """
        reflection = Reflection(cls)
        connection = Connection.getInstance(reflection.getDatabase())
        query = Query() \
            .select(reflection.getColumns()) \
            .from_(reflection.getTable())
        connection.runQuery(query)
        objects = connection.fetchAllObjects(cls)
        logging.info('Récupération de tous les modèles de la base de données.')
        return objects
    
    
    @classmethod
    def size(cls) -> int:
        """Récupération du nombre de modèles dans la base de données.

        Returns:
            int: Le nombre de modèles.
        """
        reflection = Reflection(cls)
        connection = Connection.getInstance(reflection.getDatabase())
        query = Query() \
            .select('COUNT(1)') \
            .from_(reflection.getTable())
        connection.runQuery(query)
        size = list(connection.fetchOne().values())[0]
        logging.info('Récupération du nombre de modèles dans la base de données.')
        return size    
    
    
    @classmethod
    def clear(cls) -> None:
        """Vidage de la table des modèles.
        """
        reflection = Reflection(cls)
        connection = Connection.getInstance(reflection.getDatabase())
        query = Query().truncate(reflection.getTable())
        connection.runQuery(query)
        logging.info('Vidage de la table des modèles dans la base de données.')
    
    
    @classmethod
    def execute(cls, query : Query, parameters : tuple = None) -> None:
        """Exécution d'une requête.

        Args:
            query (Query): La requête.
            parameters (tuple, optional): Les paramètres. Par défaut None.
        """
        reflection = Reflection(cls)
        connection = Connection.getInstance(reflection.getDatabase())
        connection.runQuery(query, parameters)
        logging.info('Exécution d\'une requête sur la table des modèles dans la base de données.')

    
    def create(self) -> None:
        """Création d'un modèle dans la base de données.
        """
        reflection = Reflection(self)
        connection = Connection.getInstance(reflection.getDatabase())
        query = Query().insert(reflection.getTable(), reflection.getColumns(), Reflection.generateMark(reflection.getValues()))
        connection.runQuery(query, reflection.getValues())
        logging.info('Création d\'un modèle dans la base de données.')
        
        
    def update(self, column : Union[str, tuple] = None, clause: Union[Clause, tuple] = Clause.EQUAL) -> None:
        """Mise à jour d'un modèle dans la base de données.

        Args:
            column (Union[str, tuple], optional): La ou les colonnes à prendre en compte. Par défaut None.
            clause (Union[Clause, tuple], optional): Le ou les types de clause. Par défaut Clause.EQUAL.
        """
        reflection = Reflection(self)
        connection = Connection.getInstance(reflection.getDatabase())
        query = Query().update(reflection.getTable(), reflection.getColumns(), Reflection.generateMark(reflection.getValues()))
        where, values = self.__findClause(column, clause)
        connection.runQuery(Query(f'{str(query)} {where}'), reflection.getValues() + values)
        logging.info('Mise à jour d\'un modèle dans la base de données.')
        

    def delete(self, column : Union[str, tuple] = None, clause: Union[Clause, tuple] = Clause.EQUAL) -> None:
        """Suppression d'un modèle dans la base de données.

        Args:
            column (Union[str, tuple], optional): La ou les colonnes à prendre en compte. Par défaut None.
            clause (Union[Clause, tuple], optional): Le ou les types de clause. Par défaut Clause.EQUAL.
        """
        reflection = Reflection(self)
        connection = Connection.getInstance(reflection.getDatabase())
        query = Query().delete(reflection.getTable())
        where, values = self.__findClause(column, clause)
        connection.runQuery(Query(f'{str(query)} {where}'), values)
        logging.info('Suppression d\'un modèle dans la base de données.')
        
        
    def read(self, column : Union[str, tuple] = None, clause: Union[Clause, tuple] = Clause.EQUAL) -> object:
        """Lecture d'un modèle dans la base de données.

        Args:
            column (Union[str, tuple], optional): La ou les colonnes à prendre en compte. Par défaut None.
            clause (Union[Clause, tuple], optional): Le ou les types de clause. Par défaut Clause.EQUAL.
            
        Returns:
            object: L'objet modèle lu.
        """
        reflection = Reflection(self)
        connection = Connection.getInstance(reflection.getDatabase())
        query = Query() \
            .select(reflection.getColumns()) \
            .from_(reflection.getTable())
        where, values = self.__findClause(column, clause)
        connection.runQuery(Query(f'{str(query)} {where}'), values)
        object = connection.fetchOneObject(self.__class__)
        logging.info('Lecture d\'un modèle dans la base de données.')
        return object
    
    
    def many(self, column : Union[str, tuple] = None, clause: Union[Clause, tuple] = Clause.EQUAL) -> list:
        """Lecture de plusieurs modèles dans la base de données.

        Args:
            column (Union[str, tuple], optional): La ou les colonnes à prendre en compte. Par défaut None.
            clause (Union[Clause, tuple], optional): Le ou les types de clause. Par défaut Clause.EQUAL.
            
        Returns:
            list: La liste des objets modèles lus.
        """
        reflection = Reflection(self)
        connection = Connection.getInstance(reflection.getDatabase())
        query = Query() \
            .select(reflection.getColumns()) \
            .from_(reflection.getTable())
        where, values = self.__findClause(column, clause)
        connection.runQuery(Query(f'{str(query)} {where}'), values)
        objects = connection.fetchAllObjects(self.__class__)
        logging.info('Lecture de plusieurs modèles dans la base de données.')
        return objects
    

    def exists(self, column : Union[str, tuple] = None, clause: Union[Clause, tuple] = Clause.EQUAL) -> bool:
        """Vérification de l'existence d'un modèle dans la base de données.

        Args:
            column (Union[str, tuple], optional): La ou les colonnes à prendre en compte. Par défaut None.
            clause (Union[Clause, tuple], optional): Le ou les types de clause. Par défaut Clause.EQUAL.

        Returns:
            bool: True si le modèle existe, False sinon.
        """
        reflection = Reflection(self)
        connection = Connection.getInstance(reflection.getDatabase())
        query = Query() \
            .select('1') \
            .from_(reflection.getTable())
        where, values = self.__findClause(column, clause)
        connection.runQuery(Query(f'{str(query)} {where}'), values)
        object = connection.fetchOneObject(self.__class__)
        logging.info('Vérification de l\'existence d\'un modèle dans la base de données.')
        return object is not None
    
    
    def count(self, column : Union[str, tuple] = None, clause: Union[Clause, tuple] = Clause.EQUAL) -> int:
        """Compte le nombre de modèles dans la base de données.

        Args:
            column (Union[str, tuple], optional): La ou les colonnes à prendre en compte. Par défaut None.
            clause (Union[Clause, tuple], optional): Le ou les types de clause. Par défaut Clause.EQUAL.

        Returns:
            int: Le nombre de modèles.
        """
        reflection = Reflection(self)
        connection = Connection.getInstance(reflection.getDatabase())
        query = Query() \
            .select('COUNT(1)') \
            .from_(reflection.getTable())
        where, values = self.__findClause(column, clause)
        connection.runQuery(Query(f'{str(query)} {where}'), values)
        count = list(connection.fetchOne().values())[0]
        logging.info('Compte le nombre de modèles dans la base de données.')
        return count
    
    
    def __findClause(self, column : Union[str, tuple] = None, clause: Union[Clause, tuple] = Clause.EQUAL) -> tuple:
        """Construction de la clause WHERE.

        Args:
            column (Union[str, tuple]): La ou les colonnes.
            clause (Union[Clause, tuple], optional): Le ou les types de clause. Par défaut Clause.EQUAL.

        Returns:
            tuple: La clause WHERE et les valeurs.
        """
        query = Query()
        if column is None:
            reflection = Reflection(self)
            column = reflection.getKeys()
            values = reflection.getKeysValues()
        else:
            values = getattr(self, column) \
                if not type(column) is tuple \
                else tuple(getattr(self, column) for column in column)
            
        if type(column) is tuple and type(clause) is tuple:
            for i in range(len(column)):
                if i == 0: query.where(column[i], '%s', clause[i])
                else: query.and_(column[i], '%s', clause[i])
                
        elif type(column) is tuple:
            for i in range(len(column)):
                if i == 0: query.where(column[i], '%s', clause)
                else: query.and_(column[i], '%s', clause)
                
        elif type(clause) is tuple:
            for i in range(len(clause)):
                if i == 0: query.where(column, '%s', clause[i])
                else: query.and_(column, '%s', clause[i])
                
        else:
            query.where(column, '%s', clause)
                    
        return (query, values)