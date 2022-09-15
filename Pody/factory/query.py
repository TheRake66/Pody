import logging
from Pody.factory.clause import Clause
from Pody.factory.direction import Direction
from Pody.factory.join import Join


class Query:
    """Gestion des la fabrication des requêtes
    """
    
    
    def  __init__(self) -> None:
        """Constructeur de la classe.
        """
        self.__query = ''
    
    
    def __str__(self) -> str:
        """Retourne la requête.
        
        Returns:
            str: La requête.
        """
        return self.__query
    
    
    def select(self, columns : tuple = None) -> 'Query':
        """Ajoute la clause SELECT à la requête.
        
        Args:
            columns (tuple): Liste des colonnes à sélectionner.
        
        Returns:
            Query: Instance de la classe.
        """
        self.__query += 'SELECT '
        if columns is None:
            self.__query += '*'
        else:
            for column in columns:
                self.__query += f'{column}, '
            self.__query = self.__query[:-2]
        return self
    
    
    def from_(self, tables : tuple) -> 'Query':
        """Ajoute la clause FROM à la requête.
        
        Args:
            tables (tuple): Liste des tables à sélectionner.
        
        Returns:
            Query: Instance de la classe.
        """
        self.__query += ' FROM '
        if type(tables) is tuple():
            for table in tables:
                self.__query += f'{table}, '
            self.__query = self.__query[:-2]
        else:
            self.__query += tables
        return self
    
    
    def where(self, column : str, value : str, type : Clause = Clause.EQUAL) -> 'Query':
        """Ajoute la clause WHERE à la requête.
        
        Args:
            column (str): Nom de la colonne.
            value (str): Valeur de la colonne.
            type (Clause, optional): Type de la clause. Par défaut Clause.EQUAL.
        
        Returns:
            Query: Instance de la classe.
        """
        self.__query += f' WHERE {column} {type} {value}'
        return self
    
    
    def and_(self, column : str, value : str, type : Clause = Clause.EQUAL) -> 'Query':
        """Ajoute la clause AND à la requête.
        
        Args:
            column (str): Nom de la colonne.
            value (str): Valeur de la colonne.
            type (Clause, optional): Type de la clause. Par défaut Clause.EQUAL.
        
        Returns:
            Query: Instance de la classe.
        """
        self.__query += f' AND {column} {type} {value}'
        return self
    
    
    def or_(self, column : str, value : str, type : Clause = Clause.EQUAL) -> 'Query':
        """Ajoute la clause OR à la requête.
        
        Args:
            column (str): Nom de la colonne.
            value (str): Valeur de la colonne.
            type (Clause, optional): Type de la clause. Par défaut Clause.EQUAL.
        
        Returns:
            Query: Instance de la classe.
        """
        self.__query += f' OR {column} {type} {value}'
        return self
    
    
    def on(self, column1 : str, column2 : str) -> 'Query':
        """Ajoute la clause ON à la requête.
        
        Args:
            column1 (str): Nom de la colonne.
            column2 (str): Nom de la colonne.
        
        Returns:
            Query: Instance de la classe.
        """
        self.__query += f' ON {column1} = {column2}'
        return self
    
    
    def join(self, table : str, type : Join = Join.INNER) -> 'Query':
        """Ajoute la clause JOIN à la requête.
        
        Args:
            table (str): Nom de la table.
            type (Join, optional): Type de la jointure. Par défaut Join.INNER.
        
        Returns:
            Query: Instance de la classe.
        """
        self.__query += f' {type} JOIN {table}'
        return self
    
    
    def having(self, column : str, value : str, type : Clause = Clause.EQUAL) -> 'Query':
        """Ajoute la clause HAVING à la requête.
        
        Args:
            column (str): Nom de la colonne.
            value (str): Valeur de la colonne.
            type (Clause, optional): Type de la clause. Par défaut Clause.EQUAL.
        
        Returns:
            Query: Instance de la classe.
        """
        self.__query += f' HAVING {column} {type} {value}'
        return self
    
    
    def group(self, columns : tuple) -> 'Query':
        """Ajoute la clause GROUP BY à la requête.
        
        Args:
            columns (tuple): Liste des colonnes.
        
        Returns:
            Query: Instance de la classe.
        """
        self.__query += ' GROUP BY '
        if type(columns) is tuple():
            for column in columns:
                self.__query += f'{column}, '
            self.__query = self.__query[:-2]
        else:
            self.__query += columns
        return self
    
    
    def order(self, columns : tuple, direction : Direction = Direction.ASC) -> 'Query':
        """Ajoute la clause ORDER BY à la requête.
        
        Args:
            columns (tuple): Liste des colonnes.
            direction (Direction, optional): Direction de tri. Par défaut Direction.ASC.
        
        Returns:
            Query: Instance de la classe.
        """
        self.__query += ' ORDER BY '
        if type(columns) is tuple():
            for column in columns:
                self.__query += f'{column}, '
            self.__query = self.__query[:-2]
        else:
            self.__query += columns
        self.__query += f' {direction}'
        return self
            
    
    def limit(self, count : int, offset : int = 0) -> 'Query':
        """Ajoute la clause LIMIT à la requête.
        
        Args:
            count (int): Nombre de lignes à sélectionner.
            offset (int, optional): Nombre de lignes à sauter. Par défaut 0.
        
        Returns:
            Query: Instance de la classe.
        """
        self.__query += f' LIMIT {offset}, {count}'
        return self
    
    
    def insert(self, table : str, columns : tuple, values : tuple) -> 'Query':
        """Ajoute la clause INSERT INTO à la requête.
        
        Args:
            table (str): Nom de la table.
            columns (tuple): Liste des colonnes.
            values (tuple): Liste des valeurs.
        
        Returns:
            Query: Instance de la classe.
        """
        self.__query += f'INSERT INTO {table} ('
        for column in columns:
            self.__query += f'{column}, '
        self.__query = self.__query[:-2] + ') VALUES ('
        for value in values:
            self.__query += f'{value}, '
        self.__query = self.__query[:-2] + ')'
        return self
    
    
    def update(self, table : str, columns : tuple, values : tuple) -> 'Query':
        """Ajoute la clause UPDATE à la requête.
        
        Args:
            table (str): Nom de la table.
            columns (tuple): Liste des colonnes.
            values (tuple): Liste des valeurs.
        
        Returns:
            Query: Instance de la classe.
        """
        self.__query += f'UPDATE {table} SET '
        for i in range(len(columns)):
            self.__query += f'{columns[i]} = {values[i]}, '
        self.__query = self.__query[:-2]
        return self
    
    
    def delete(self, table : str) -> 'Query':
        """Ajoute la clause DELETE FROM à la requête.
        
        Args:
            table (str): Nom de la table.
        
        Returns:
            Query: Instance de la classe.
        """
        self.__query += f'DELETE FROM {table}'
        return self