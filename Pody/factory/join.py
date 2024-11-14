from enum import Enum



class Join(Enum):
    """Enumeration of join types.
    """
    
    INNER: str = 'INNER'
    LEFT: str = 'LEFT'
    RIGHT: str = 'RIGHT'
    FULL: str = 'FULL'