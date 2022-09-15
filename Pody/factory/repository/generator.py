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
        configuration = self.__connection.getConfigurations()
        database = configuration.getDatabase().lower()
        logging.info(f'Génération du du modèle "{database}"...')
        if not os.path.exists(database):
            logging.info(f'Création du dépôt "{database}"...')
            os.makedirs(database)
        
        if tables is None:
            tables = self.__connection.runQuery('SHOW TABLES').fetchAll()
        elif type(tables) is str:
            tables = (tables,)
            
        for table in tables:
            name = list(table.values())[0].lower()
                
            model = f'{database}/{name}.py'
            if not os.path.exists(model):
                logging.info(f'Génération du modèle "{name}"...')
                with open(model, mode="w", encoding="utf-8") as file:
                        
                    file.write(f'''from datetime import datetime
from Pody.factory.repository.model import Model
                            
                            
                        
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
                        name = column['Field'].lower()
                        type = column['Type'].split('(')[0].lower()
                        default = column['Default']
                        key = column['Key']
                        extra = column['Extra']
                        null = column['Null']
                        
                        logging.info(f'Génération de l\'attribut "{name}"...')
                        
                        if key == 'PRI':
                            name = f'_{name}'
                        
                        if type in [ 'varchar', 'char', 'text' ]:
                            type = 'str'
                        elif type in [ 'double', 'decimal' ]:
                            type = 'float'
                        elif type in [ 'tinyint' ]:
                            type = 'bool'
                        elif type in [ 'smallint', 'int', 'mediumint', 'bigint' ]:
                            type = 'int'
                        elif type in [ 'date', 'datetime', 'timestamp' ]:
                            type = 'datetime'
                        else:
                            type = 'str'
                            
                        if default is None:
                            default = 'None'
                        elif type == 'str':
                            default = f"'{default}'"
                        elif type == 'bool':
                            default = 'True' if default else 'False'
                        elif type == 'datetime':
                            default = f'datetime.datetime({default.year}, {default.month}, {default.day}, {default.hour}, {default.minute}, {default.second})'
                        elif type == 'date':
                            default = f'datetime.date({default.year}, {default.month}, {default.day})'
                        elif type == 'time':
                            default = f'datetime.time({default.hour}, {default.minute}, {default.second})'
                        
                        parameters.append(f',\n        {name} : {type} = {default}')
                        attributes.append(f'\n        self.{name} = {name}')
             
                    parameters = ''.join(parameters)
                    attributes = ''.join(attributes)
                    file.write(f'    def __init__(self{parameters}):{attributes}')
                    
        logging.info('Génération terminée.')