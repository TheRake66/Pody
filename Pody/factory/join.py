import logging


class Join:
    """Enumération des types de jointure.
    """
    
    INNER = 'INNER'  # type: int # INNER JOIN
    LEFT = 'LEFT'    # type: int # LEFT JOIN
    RIGHT = 'RIGHT'  # type: int # RIGHT JOIN
    FULL = 'FULL'    # type: int # FULL JOIN