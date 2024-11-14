from pody.factory.clause import Clause
from pody.factory.direction import Direction
from pody.factory.join import Join



class Query:
    """Query manufacturing object.
    """
    
    
    def  __init__(self, query: str = '') -> None:
        """Constructor of the class.
        
        Arguments:
            query (str, optional): Query. Default is ''.
        """
        self.__query = query
    
    
    def __str__(self) -> str:
        """Representation of the query object.
        
        Returns:
            str: Query.
        """
        return self.__query.strip()
    
    
    def select(self, columns: tuple | str | None = None) -> 'Query':
        """Adds a SELECT clause to the query.
        
        Arguments:
            columns (tuple | str | None): Column name or list of columns names to select. None to alls. Default is None.
        
        Returns:
            Query: Instance of the class.
        """
        self.__addToQuery('SELECT')
        if columns is None:
            self.__addToQuery('*')
        elif not type(columns) is tuple:
            self.__addToQuery(columns)
        else:
            self.__addTupleToQuery(columns)
        return self
    
    
    def from_(self, tables: tuple) -> 'Query':
        """Adds a FROM clause to the query.
        
        Arguments:
            tables (tuple | str): Table name or list of tables names to search.
        
        Returns:
            Query: Instance of the class.
        """
        self.__addToQuery('FROM')
        if not type(tables) is tuple:
            self.__addToQuery(tables)
        else:
            self.__addTupleToQuery(tables)
        
    
    def where(self, column: str, value: str, type: Clause = Clause.EQUAL) -> 'Query':
        """Adds a WHERE clause to the query.
        
        Arguments:
            column (str): Column name.
            value (str): Column value.
            type (Clause, optional): Clause type. Default is Clause.EQUAL.
        
        Returns:
            Query: Instance of the class.
        """
        self.__addToQuery(f'WHERE {column} {type} {value}')
        return self
    
    
    def and_(self, column: str, value: str, type: Clause = Clause.EQUAL) -> 'Query':
        """Adds a AND clause to the query.
        
        Arguments:
            column (str): Column name.
            value (str): Column value.
            type (Clause, optional): Clause type. Default is Clause.EQUAL.
        
        Returns:
            Query: Instance of the class.
        """
        self.__addToQuery(f'AND {column} {type} {value}')
        return self
    
    
    def or_(self, column: str, value: str, type: Clause = Clause.EQUAL) -> 'Query':
        """Adds a OR clause to the query.
        
        Arguments:
            column (str): Column name.
            value (str): Column value.
            type (Clause, optional): Clause type. Default is Clause.EQUAL.
        
        Returns:
            Query: Instance of the class.
        """
        self.__addToQuery(f'OR {column} {type} {value}')
        return self
    
    
    def on(self, column1: str, column2: str) -> 'Query':
        """Adds a ON clause to the query.
        
        Arguments:
            column1 (str): First column name.
            column2 (str): Second column name.
        
        Returns:
            Query: Instance of the class.
        """
        self.__addToQuery(f'ON {column1} = {column2}')
        return self
    
    
    def join(self, table: str, type: Join = Join.INNER) -> 'Query':
        """Adds a JOIN clause to the query.
        
        Arguments:
            table (str): Table name.
            type (Join, optional): Join type. Default is Join.INNER.
        
        Returns:
            Query: Instance of the class.
        """
        self.__addToQuery(f'{type} JOIN {table}')
        return self
    
    
    def having(self, column: str, value: str, type: Clause = Clause.EQUAL) -> 'Query':
        """Adds a HAVING clause to the query.
        
        Arguments:
            column (str): Column name.
            value (str): Column value.
            type (Clause, optional): Clause type. Default is Clause.EQUAL.
        
        Returns:
            Query: Instance of the class.
        """
        self.__addToQuery(f'HAVING {column} {type} {value}')
        return self
    
    
    def group(self, columns: tuple | str) -> 'Query':
        """Adds a GROUP BY clause to the query.
        
        Arguments:
            columns (tuple | str): Column name or list of columns names to group by.
        
        Returns:
            Query: Instance of the class.
        """
        self.__addToQuery('GROUP BY')
        if not type(columns) is tuple:
            self.__addToQuery(columns)
        else:
            self.__addTupleToQuery(columns)
        return self
    
    
    def order(self, columns: tuple | str, direction: Direction = Direction.ASCENDING) -> 'Query':
        """Adds a ORDER BY clause to the query.
        
        Arguments:
            columns (tuple | str): Column name or list of columns names to group by.
            direction (Direction, optional): Sort direction. Default is Direction.ASCENDING.
        
        Returns:
            Query: Instance of the class.
        """
        self.__addToQuery('ORDER BY')
        if not type(columns) is tuple:
            self.__addToQuery(columns)
        else:
            self.__addTupleToQuery(columns)
        self.__addToQuery(direction)
        return self
            
    
    def limit(self, count: int, offset: int = 0) -> 'Query':
        """Adds a LIMIT clause to the query.
        
        Arguments:
            count (int): Number of lines to select.
            offset (int, optional): Number of lines to skip. Default 0.
        
        Returns:
            Query: Instance of the class.
        """
        self.__addToQuery(f'LIMIT {offset}, {count}')
        return self
    
    
    def insert(self, table: str, columns: tuple | str) -> 'Query':
        """Adds a INSERT INTO clause to the query.
        
        Arguments:
            table (str): Table name.
            columns (tuple | str): Column name or list of columns names.
        
        Returns:
            Query: Instance of the class.
        """
        self.__addToQuery(f'INSERT INTO {table} (')
        if not type(columns) is tuple:
            self.__addToQuery(columns)
        else:
            self.__addTupleToQuery(columns)
        self.__addToQuery(f')')
        return self
    
    
    def values(self, values: tuple | str) -> 'Query':
        """Adds a VALUES clause to the query.
        
        Arguments:
            values (tuple | str): Value or values.
        
        Returns:
            Query: Instance of the class.
        """
        self.__addToQuery(f'VALUES (')
        if not type(values) is tuple:
            self.__addToQuery(values)
        else:
            self.__addTupleToQuery(values)
        self.__addToQuery(f')')
        return self
    
    
    def update(self, table : str, columns : tuple, values : tuple) -> 'Query':
        """Ajoute la clause UPDATE à la requête.
        
        Arguments:
            table (str): Nom de la table.
            columns (tuple): Liste des colonnes.
            values (tuple): Liste des valeurs.
        
        Returns:
            Query: Instance of the class.
        """
        self.__query += f'UPDATE {table} SET '
        for i in range(len(columns)):
            self.__query += f'{columns[i]} = {values[i]}, '
        self.__query = f'{self.__query[:-2]} '
        return self
    
    
    def delete(self, table : str) -> 'Query':
        """Ajoute la clause DELETE FROM à la requête.
        
        Arguments:
            table (str): Nom de la table.
        
        Returns:
            Query: Instance of the class.
        """
        self.__query += f'DELETE FROM {table} '
        return self
    
    
    def truncate(self, table : str) -> 'Query':
        """Ajoute la clause TRUNCATE TABLE à la requête.
        
        Arguments:
            table (str): Nom de la table.
        
        Returns:
            Query: Instance of the class.
        """
        self.__query += f'TRUNCATE TABLE {table} '
        return self
    
    
    def drop(self, table : str) -> 'Query':
        """Ajoute la clause DROP TABLE à la requête.
        
        Arguments:
            table (str): Nom de la table.
        
        Returns:
            Query: Instance of the class.
        """
        self.__query += f'DROP TABLE {table} '
        return self
    
    
    def bopen(self) -> 'Query':
        """Ajoute une parenthèse ouvrante à la requête.
        
        Returns:
            Query: Instance of the class.
        """
        self.__query += '( '
        return self
    
    
    def bclose(self) -> 'Query':
        """Ajoute une parenthèse fermante à la requête.
        
        Returns:
            Query: Instance of the class.
        """
        self.__query += ') '
        return self
    
    
    
    
    
    
    
    
    def __addToQuery(self, value: str) -> None:
        """Adds a value to the query.

        Args:
            value (str): Value.
        """
        self.__query += f'{value} '
    
    
    def __addTupleToQuery(self, values: tuple) -> None:
        """Adds a list of values to the query, separating them with commas.

        Arguments:
            values (tuple): List of values.
        """
        for value in values:
            self.__query += f'{value}, '
        self.__query = f'{self.__query[:-2]} '