import logging
import os
from typing import Union

from Pody.connection import Connection


    
class Generator:
    """Librairie de génération de modèles.
    """
    
    
    def __init__(self) -> None:
        """Constructeur de la classe.
        """
        self.__connection = Connection.getCurrent()
        
        
    def generate(self, tables : Union[str, tuple] = None) -> None:
        """Génère un modèle à partir d'une table.
        
        Args:
            tables (Union[str, tuple]): Le nom de la table ou les tables. Si None, toutes les tables seront générées.
        """
        database = self.__connection.getConfigurations().getDatabase().lower()
        if not os.path.exists(database):
            logging.info(f'Création du dépôt "{database}"...')
            os.makedirs(database)
        
        if tables is None:
            tables = self.__connection.runQuery('SHOW TABLES').fetchAll()
        elif type(tables) is str:
            tables = (tables,)
            
        for table in tables:
            if type(table) is dict:
                table = list(table.values())
            name = table[0].lower()
                
            logging.info(f'Génération du modèle "{name}"...')
            model = f'{database}/{name}.py'
            if not os.path.exists(model):
                with open(model, mode="w", encoding="utf-8") as file:
                        
                    file.write(f'''from Pody.factory.repository.model import Model
                            
                        
class {name.capitalize()}(Model):
    """Modèle de la table "{name}".

    Args:
        Model (Model): Modèle de base.
    """

    
''')
                    
                    columns = self.__connection.runQuery(f'SHOW COLUMNS FROM {name}').fetchAll()
                    parameters = []
                    attributes = []
                    for column in columns:        
                        if type(column) is dict:
                            column = list(column.values())                
                        name, type_, null, key, default, extra = column
                        
                        logging.info(f'Génération de l\'attribut "{name}"...')
                        
                        if key == 'PRI':
                            name = f'_{name}'
                        
                        type_ = type_.split('(')[0].lower()
                        if type_ in [ 'varchar', 'char', 'text' ]:
                            type_ = 'str'
                        elif type_ in [ 'double', 'decimal' ]:
                            type_ = 'float'
                        elif type_ in [ 'tinyint', 'smallint' ]:
                            type_ = 'bool'
                            
                        if default is None:
                            default = 'None'
                        elif type_ == 'str':
                            default = f"'{default}'"
                        elif type_ == 'bool':
                            default = 'True' if default else 'False'
                        elif type_ == 'datetime':
                            default = f'datetime.datetime({default.year}, {default.month}, {default.day}, {default.hour}, {default.minute}, {default.second})'
                        elif type_ == 'date':
                            default = f'datetime.date({default.year}, {default.month}, {default.day})'
                        elif type_ == 'time':
                            default = f'datetime.time({default.hour}, {default.minute}, {default.second})'
                        
                        parameters.append(f',\n        {name} : {type_} = {default}')
                        attributes.append(f'\n        self.{name} = {name}')
             
                    parameters = ''.join(parameters)
                    attributes = ''.join(attributes)
                    file.write(f'    def __init__(self{parameters}):{attributes}')
                    
        logging.info('Génération terminée.')