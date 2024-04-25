from enum import Enum

class Color(Enum):
    RED = 1
    BLACK = 2

class Arc:
    def __init__(self):
        # used for balancing
        self.color = Color.RED

        # hierarchy
        self.parent = None # Arc
        self.left = None # Arc
        self.right = None # Arc

        # diagram
        self.site = None # dcel.site
        self.left_half_edge = None # dcel.half_edge
        self.right_hal_edge = None # dcel.half_edge
        self.event = None # Event

        self.prev = None # Arc
        self.next = None # Arc

