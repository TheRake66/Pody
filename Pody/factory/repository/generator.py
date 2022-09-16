import logging
import os
from typing import Union

from Pody.connection import Connection


    
class Generator:
    """Librairie de génération de modèles.
    """
    
    
    def __init__(self, connection : Connection) -> None:
        """Constructeur de la classe.
        
        Args:
            connection (Connection): La connexion à la base de données.
        """
        self.__connection = connection
        
        
    def generateModels(self, tables : Union[str, tuple] = None) -> None:
        """Génère un modèle à partir d'une table.
        
        Args:
            tables (Union[str, tuple]): Le nom de la table ou les tables. Si None, toutes les tables seront générées.
        """
        configuration = self.__connection.getConfigurations()
        database = configuration.getDatabase().lower()
        if not os.path.exists(database):
            logging.info(f'Création du dépôt "{database}"...')
            os.makedirs(database)
            logging.info(f'Le dépôt a été créé.')
        
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
                        
                    file.write(f'from datetime import datetime\n')
                    file.write(f'from Pody.factory.repository.model import Model\n')
                    file.write('\n')
                    file.write('\n')
                    file.write('\n')
                    file.write(f'class {name.capitalize()}(Model):\n')
                    file.write(f'    """Modèle de la table "{name}".\n')
                    file.write('\n')
                    file.write(f'    Args:\n')
                    file.write(f'        Model (Model): Modèle de base.\n')
                    file.write(f'    """\n')
                    file.write('\n')
                    file.write('\n')
                    
                    columns = self.__connection.runQuery(f'SHOW COLUMNS FROM {name}').fetchAll()
                    parameters = []
                    attributes = []
                    docstring = []
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
                        docstring.append(f'\n            {name} ({type}, optional): Le champs "{name}". Par défaut {default}.')

                        logging.info(f'L\'attribut a été généré.')
                
                    parameters = ''.join(parameters)
                    attributes = ''.join(attributes)
                    docstring = ''.join(docstring)
                    
                    file.write(f'    def __init__(self{parameters}):\n')
                    file.write(f'        """Constructeur de la classe.\n')
                    file.write('\n')
                    file.write(f'        Args:\n')
                    file.write(f'            {docstring}\n')
                    file.write(f'        """')
                    file.write(f'        {attributes}')
                logging.info(f'Le modèle a été généré.')