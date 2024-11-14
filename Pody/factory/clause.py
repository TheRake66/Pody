from enum import Enum



class Clause(Enum):
    """List of clause types.
    """
    
    NONE: str = ' '
    LESS: str = '<'
    GREATER: str = '>'
    EQUAL: str = '='
    LIKE: str = 'LIKE'
    IS: str = 'IS'
    IN: str = 'IN'
    NOT: str = 'NOT'
    