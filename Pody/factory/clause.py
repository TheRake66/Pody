import logging


class Clause:
    """Enumération des types de clause.
    """
    
    NONE = ' '     # type: str # Clause vide
    LESS = '<'     # type: str # <
    GREATER = '>'  # type: str # >
    EQUAL = '='    # type: str # =
    LIKE = 'LIKE'  # type: str # LIKE
    IS = 'IS'      # type: str # IS
    IN = 'IN'      # type: str # IN
    NOT = 'NOT'    # type: str # NOT
    