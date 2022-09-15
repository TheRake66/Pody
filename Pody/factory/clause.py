import logging


class Clause:
    """Enumération des types de clause.
    """
    
    LESS = '<'     # type: int # <
    GREATER = '>'  # type: int # >
    EQUAL = '='    # type: int # =
    LIKE = 'LIKE'     # type: int # LIKE