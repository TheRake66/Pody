from typing import Union



class Reflection:
    """Gestion de la réflexion entre le modèle et la base de données
    """
    
    
    def __init__(self, model : Union[object, type]) -> None:
        """Constructor of the class.

        Arguments:
            model (Union[object, type]): Modèle à réfléchir.
        """
        if type(model) is type:
            model = model()
        self.__model = model
    

    def getDatabase(self) -> str:
        """Retourne le nom de la base de données liée au modèle.
        
        Returns:
            str: Nom de la base de données liée au modèle.
        """
        return self.__model.__module__.split('.')[0]
    
    
    def getTable(self) -> str:
        """Retourne le nom de la table liée au modèle.
        
        Returns:
            str: Nom de la table liée au modèle.
        """
        return self.__model.__class__.__name__.lower()
    
    
    def getColumns(self) -> tuple:
        """Retourne les noms des colonnes liées au modèle.
        
        Returns:
            tuple: Noms des colonnes liées au modèle.
        """
        return tuple(Reflection.parseKey(attribute) for attribute in self.__model.__dict__)
    
    
    def getValues(self) -> tuple:
        """Retourne la liste des valeurs liées au modèle.
        
        Returns:
            tuple: Liste des valeurs liées au modèle.
        """
        return tuple(getattr(self.__model, attribute) for attribute in self.__model.__dict__)
    
    
    def getKeys(self) -> tuple:
        """Retourne la liste des clés primaires liées au modèle.
        
        Returns:
            tuple: Liste des clés primaires liées au modèle.
        """
        primary = []
        for attribute in self.__model.__dict__:
            if attribute[0] == '_':
                primary.append(Reflection.parseKey(attribute))
        return tuple(primary)
        
    
    def getKeysValues(self) -> tuple:
        """Retourne la liste valeurs des clés primaires liées au modèle.
        
        Returns:
            tuple: Liste des valeurs des clés primaires liées au modèle.
        """
        values = []
        for attribute in self.__model.__dict__:
            if attribute[0] == '_':
                values.append(getattr(self.__model, attribute))
        return tuple(values)
    
    
    def getFields(self) -> tuple:
        """Retourne la liste des champs liés au modèle.
        
        Returns:
            tuple: Liste des champs liés au modèle.
        """
        fields = []
        for attribute in self.__model.__dict__:
            if attribute[0] != '_':
                fields.append(attribute)
        return tuple(fields)
        
    
    def getFieldsValues(self) -> tuple:
        """Retourne la liste des valeurs des champs liés au modèle.
        
        Returns:
            list: Liste des valeurs des champs liés au modèle.
        """
        values = []
        for attribute in self.__model.__dict__:
            if attribute[0] != '_':
                values.append(getattr(self.__model, attribute))
        return tuple(values)
        
    
    @classmethod
    def parseKey(cls, key : str) -> str:
        """Parse une clé primaire.
        
        Arguments:
            key (str): Clé primaire à parser.
        
        Returns:
            tuple: Clé primaire parsée.
        """
        return key[1:] if key[0] == '_' else key
    
    
    @classmethod
    def generateMark(cls, columns : list) -> tuple:
        """Génère une chaine de caractères de marqueurs.
        
        Arguments:
            columns (list): Liste des colonnes à utiliser.
        
        Returns:
            tuple: Liste de caractères de marqueurs.
        """
        return tuple('%s' for _ in columns)