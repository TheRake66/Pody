import logging



class Converter:
    """Librairie de conversion de données vers des modèles.
    """
    
    
    def __init__(self, class_ : type) -> None:
        """Constructeur de la classe.

        Arguments:
            class_ (type): Le modèle à convertir.
        """
        self.__model = class_
        
        
    def convertWith(self, data : dict) -> object:
        """Convertit les données vers le modèle.

        Arguments:
            data (dict): Les données à convertir.

        Returns:
            object: Le modèle converti.
        """
        newmodel = self.__model()
        for key, value in data.items():
            if hasattr(newmodel, key):
                setattr(newmodel, key, value)
            elif hasattr(newmodel, f'_{key}'):
                setattr(newmodel, f'_{key}', value)
            else:
                logging.warning(f'La propriété "{key}" n\'existe pas dans le modèle "{self.__model.__class__.__name__}".')
        return newmodel