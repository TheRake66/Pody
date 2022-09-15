import logging

from Pody.connection import Connection
from Pody.factory.clause import Clause
from Pody.factory.query import Query
from Pody.factory.repository.reflection import Reflection


class Model:
    """Gestion des méthodes liées au modèle de données.
    """
    
    
    def create(self) -> None:
        """Création d'un modèle dans la base de données.
        """
        reflection = Reflection(self)
        connection = Connection.getInstance(reflection.getDatabase())
        query = Query().insert(reflection.getTable(), reflection.getColumns(), Reflection.generateMark(reflection.getValues()))
        connection.runQuery(query, reflection.getValues())
        logging.info('Création d\'un modèle dans la base de données.')
        
        
    def update(self, columns : tuple = None, clause : Clause =  Clause.EQUAL) -> None:
        """Mise à jour d'un modèle dans la base de données.

        Args:
            columns (tuple, optional): Clause de mise à jour. Par défaut None.
            clause (Clause, optional): Type de clause. Par défaut Clause.EQUAL.
        """
        reflection = Reflection(self)
        connection = Connection.getInstance(reflection.getDatabase())
        query = Query().update(reflection.getTable(), reflection.getColumns(), Reflection.generateMark(reflection.getValues()))
        where, values = self.__findClause(columns, clause)
        connection.runQuery(Query(f'{str(query)} {where}'), reflection.getValues() + values)
        logging.info('Mise à jour d\'un modèle dans la base de données.')
        

    def delete(self, columns : tuple = None, clause : Clause =  Clause.EQUAL) -> None:
        """Suppression d'un modèle dans la base de données.

        Args:
            columns (tuple, optional): Clause de suppression. Par défaut None.
            clause (Clause, optional): Type de clause. Par défaut Clause.EQUAL.
        """
        reflection = Reflection(self)
        connection = Connection.getInstance(reflection.getDatabase())
        query = Query().delete(reflection.getTable())
        where, values = self.__findClause(columns, clause)
        connection.runQuery(Query(f'{str(query)} {where}'), values)
        logging.info('Suppression d\'un modèle dans la base de données.')
        
        
    def read(self, columns : tuple = None, clause : Clause =  Clause.EQUAL) -> object:
        """Lecture d'un modèle dans la base de données.

        Args:
            columns (tuple, optional): Clause de lecture. Par défaut None.
            clause (Clause, optional): Type de clause. Par défaut Clause.EQUAL.
            
        Returns:
            object: L'objet modèle lu.
        """
        reflection = Reflection(self)
        connection = Connection.getInstance(reflection.getDatabase())
        query = Query() \
            .select(reflection.getColumns()) \
            .from_(reflection.getTable())
        where, values = self.__findClause(columns, clause)
        connection.runQuery(Query(f'{str(query)} {where}'), values)
        object = connection.fetchOneObject(self.__class__)
        logging.info('Lecture d\'un modèle dans la base de données.')
        return object
    
    
    def many(self, columns : tuple = None, clause : Clause =  Clause.EQUAL) -> list:
        """Lecture de plusieurs modèles dans la base de données.

        Args:
            columns (tuple, optional): Clause de lecture. Par défaut None.
            clause (Clause, optional): Type de clause. Par défaut Clause.EQUAL.
            
        Returns:
            list: La liste des objets modèles lus.
        """
        reflection = Reflection(self)
        connection = Connection.getInstance(reflection.getDatabase())
        query = Query() \
            .select(reflection.getColumns()) \
            .from_(reflection.getTable())
        where, values = self.__findClause(columns, clause)
        connection.runQuery(Query(f'{str(query)} {where}'), values)
        objects = connection.fetchAllObjects(self.__class__)
        logging.info('Lecture de plusieurs modèles dans la base de données.')
        return objects
    
    
    def __findClause(self, columns : tuple, clause : Clause) -> tuple:
        """Construction de la clause WHERE.

        Args:
            columns (tuple): La liste des colonnes.
            clause (Clause): Le type de clause.

        Returns:
            tuple: _description_
        """
        query = Query()
        if columns is None:
            reflection = Reflection(self)
            columns = reflection.getKeys()
            values = reflection.getKeysValues()
        else:
            if not type(columns) is tuple:
                values = getattr(self, columns)
            else:
                values = tuple(getattr(self, column) for column in columns)
            
        if not type(columns) is tuple:
            query.where(columns, '%s', clause)
        else:
            for i in range(len(columns)):
                if i == 0:
                    query.where(columns[i], '%s', clause)
                else:
                    query.and_(columns[i], '%s', clause)
                    
        return (query, values)