from datetime import datetime
from Pody.factory.repository.model import Model



class User(Model):
    """Modèle de la table "user".

    Args:
        Model (Model): Modèle de base.
    """


    def __init__(self,
        _id : int = None,
        name : str = None,
        firstname : str = None,
        mail : str = None):
        """Constructeur de la classe.

        Args:
            
            _id (int, optional): Le champs "_id". Par défaut None.
            name (str, optional): Le champs "name". Par défaut None.
            firstname (str, optional): Le champs "firstname". Par défaut None.
            mail (str, optional): Le champs "mail". Par défaut None.
        """        
        self._id = _id
        self.name = name
        self.firstname = firstname
        self.mail = mail