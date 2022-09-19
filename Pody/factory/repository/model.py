import json
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
        query = Query() \
            .select(reflection.getColumns()) \
            .from_(reflection.getTable())
        connection = cls().__runOn(query, (), reflection)
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
        query = Query() \
            .select('COUNT(1)') \
            .from_(reflection.getTable())
        connection = cls().__runOn(query, (), reflection)
        size = list(connection.fetchOne().values())[0]
        logging.info('Récupération du nombre de modèles dans la base de données.')
        return size    
    
    
    @classmethod
    def clear(cls) -> None:
        """Vidage de la table des modèles.
        """
        reflection = Reflection(cls)
        query = Query().truncate(reflection.getTable())
        cls().__runOn(query, (), reflection)
        logging.info('Vidage de la table des modèles dans la base de données.')
    
    
    @classmethod
    def execute(cls, query : Query, parameters : tuple = None, multiple : bool = False) -> None:
        """Exécution d'une requête.

        Args:
            query (Query): La requête.
            parameters (tuple, optional): Les paramètres. Par défaut None.
            multiple (bool, optional): Indique si lors d'une insertion, plusieurs lignes doivent être insérées. Par défaut False.
        """
        cls().__runOn(query, parameters, None, multiple)
        logging.info('Exécution d\'une requête sur la table des modèles dans la base de données.')
        
    
    @classmethod
    def inject(cls, objects : list) -> None:
        """Injection de modèles dans la base de données.

        Args:
            objects (list): La liste des modèles.
        """
        reflection = Reflection(cls)
        query = Query() \
            .insert(reflection.getTable(), reflection.getColumns()) \
            .values(Reflection.generateMark(reflection.getValues()))
        cls().__runOn(query, [ Reflection(object).getValues() for object in objects ], reflection, True)
        logging.info('Injection de modèles dans la base de données.')

    
    def create(self) -> None:
        """Création d'un modèle dans la base de données.
        """
        reflection = Reflection(self)
        query = Query() \
            .insert(reflection.getTable(), reflection.getColumns()) \
            .values(Reflection.generateMark(reflection.getValues()))
        self.__runOn(query, reflection.getValues(), reflection)
        logging.info('Création d\'un modèle dans la base de données.')
        
        
    def update(self, column : Union[str, tuple] = None, clause: Union[Clause, tuple] = Clause.EQUAL) -> None:
        """Mise à jour d'un modèle dans la base de données.

        Args:
            column (Union[str, tuple], optional): La ou les colonnes à prendre en compte. Par défaut None.
            clause (Union[Clause, tuple], optional): Le ou les types de clause. Par défaut Clause.EQUAL.
        """
        reflection = Reflection(self)
        query = Query().update(reflection.getTable(), reflection.getColumns(), Reflection.generateMark(reflection.getValues()))
        where, values = self.__findClause(column, clause)
        self.__runOn(Query(f'{str(query)} {where}'), reflection.getValues() + values, reflection)
        logging.info('Mise à jour d\'un modèle dans la base de données.')
        

    def delete(self, column : Union[str, tuple] = None, clause: Union[Clause, tuple] = Clause.EQUAL) -> None:
        """Suppression d'un modèle dans la base de données.

        Args:
            column (Union[str, tuple], optional): La ou les colonnes à prendre en compte. Par défaut None.
            clause (Union[Clause, tuple], optional): Le ou les types de clause. Par défaut Clause.EQUAL.
        """
        reflection = Reflection(self)
        query = Query().delete(reflection.getTable())
        where, values = self.__findClause(column, clause)
        self.__runOn(Query(f'{str(query)} {where}'), values, reflection)
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
        query = Query() \
            .select(reflection.getColumns()) \
            .from_(reflection.getTable())
        where, values = self.__findClause(column, clause)
        connection = self.__runOn(Query(f'{str(query)} {where}'), values, reflection)
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
        query = Query() \
            .select(reflection.getColumns()) \
            .from_(reflection.getTable())
        where, values = self.__findClause(column, clause)
        connection = self.__runOn(Query(f'{str(query)} {where}'), values, reflection)
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
        query = Query() \
            .select('1') \
            .from_(reflection.getTable())
        where, values = self.__findClause(column, clause)
        connection = self.__runOn(Query(f'{str(query)} {where}'), values, reflection)
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
        query = Query() \
            .select('COUNT(1)') \
            .from_(reflection.getTable())
        where, values = self.__findClause(column, clause)
        connection = self.__runOn(Query(f'{str(query)} {where}'), values, reflection)
        count = list(connection.fetchOne().values())[0]
        logging.info('Compte le nombre de modèles dans la base de données.')
        return count
    
    
    def __runOn(self, query : Query, parameters : any = (), reflection : Reflection = None, multiple : bool = False) -> Connection:
        """Exécute une requête sur la base de données liée au modèle.

        Args:
            query (Query): La requête à exécuter.
            parameters (any, optional): Les paramètres de la requête. Par défaut ().
            reflection (Reflection, optional): La réflexion existante du modèle. Par défaut None.
            multiple (bool, optional): Indique si lors d'une insertion, plusieurs lignes doivent être insérées. Par défaut False.
            
        Returns:
            Connection: La connexion à la base de données.
        """
        if reflection is None:
            reflection = Reflection(self)
        connection = Connection.getInstance(reflection.getDatabase())
        connection.runQuery(query, parameters, multiple)
        return connection
    
    
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
            if not type(column) is tuple:
                values = getattr(self, column)
                column = Reflection.parseKey(column)
            else:
                values = tuple(getattr(self, c) for c in column)
                column = tuple(Reflection.parseKey(c) for c in column)
                
            
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
    
    
    def __str__(self):
        """Retourne le modèle au format JSON.

        Returns:
            str: Je JSON du modèle.
        """
        return json.dumps(self.__dict__)