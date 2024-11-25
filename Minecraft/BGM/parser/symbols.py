from enum import Enum
class Dir(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

def matching_dir(vec: tuple[int, int]):
    match vec:
        case (0, 1):
            return Dir.LEFT
        case (0, -1):
            return Dir.RIGHT
        case (1, 0):
            return Dir.UP
        case (-1, 0):
            return Dir.DOWN

class Gate:
    def __init__(self):
        self.inputs: set = set()

        self.z = None
        self.x = None

        self.visited: set[Dir] = set()

        ALL_OBJECTS.append(self)

    def add_input(self, i, prevZ, prevX):
        self.inputs.add(i)
        d = None
        match (self.z - prevZ, self.x - prevX):
            case (0, 1):
                d = Dir.LEFT
            case (0, -1):
                d = Dir.RIGHT
            case (1, 0):
                d = Dir.UP
            case (-1, 0):
                d = Dir.DOWN
        self.visit_branch(d)

    def visit_branch(self, d: Dir):
        if d is None: raise ValueError("Direction cannot be None")
        self.visited.add(d)

    def to_string(self):
        for i in self.inputs:
            if isinstance(i, Gate):
                i.to_string()
                print(i.__class__.__name__)
            else:
                print(i)

    symbols = {
        "OR": "|",
        "XOR": "^"
    }
    def symbol(self):
        return Gate.symbols[self.__class__.__name__]

    i = 0
    def to_algebraic(self):
        Gate.i += 1
        string = "("
        for i, child in enumerate(self.inputs):
            if isinstance(child, Entry):
                string += child.resolve()
            elif isinstance(child, Gate):
                if isinstance(child, OR):
                    # simplify OR with only one input
                    if len(child.inputs) == 1:
                        a = child.inputs.pop()
                        string += str(id(a))
                        if i != len(self.inputs) - 1:
                            string += self.symbol()
                        child.inputs.add(a)
                        continue
                for sChild in child.inputs:
                    if id(sChild) == id(self):
                        continue
                string += str(id(child))
            else:
                raise Exception("you forgot a class, dumbass")
            if i != len(self.inputs) - 1:
                string += self.symbol()
        string += ")"
        return string

    def to_literal(self):
        if isinstance(self, NAND):
            string = "Not(And("
        else:
            string = self.__class__.__name__.capitalize() + "("
        for i, child in enumerate(self.inputs):
            if isinstance(child, Entry):
                string += child.resolve()
            elif isinstance(child, Gate):
                if isinstance(child, OR):
                    # simplify OR with only one input
                    if len(child.inputs) == 1:
                        a = child.inputs.pop()
                        string += str(id(a))
                        if i != len(self.inputs) - 1:
                            string += ","
                        child.inputs.add(a)
                        continue
                for sChild in child.inputs:
                    if id(sChild) == id(self):
                        continue
                string += str(id(child))
            else:
                raise Exception("you forgot a class, dumbass")
            if i != len(self.inputs) - 1:
                string += ","
        string += ")"
        if isinstance(self, NAND):
            string += ")"
        return string

    algebraic = 0
    def resolve(self):
        if Gate.algebraic:
            return self.to_algebraic()
        else:
            return self.to_literal()

    def __str__(self):
        return self.__class__.__name__


class AND(Gate):
    def __init__(self, inputs):
        super().__init__()

    # def resolve(self):
    #     return all(self.inputs)

class NAND(Gate):
    def __init__(self, inputs):
        super().__init__()

class NOT(Gate):
    def __init__(self, theInput):
        super().__init__()

class OR(Gate):
    def __init__(self, inputs):
        super().__init__()

    # def resolve(self):
    #     return any(self.inputs)

class XOR(Gate):
    def __init__(self, inputs):
        super().__init__()

    # def resolve(self):
    #     return sum(self.inputs) % 2


class Wire:
    def __init__(self, expr):
        self.expr = expr

class Entry:
    entry_counter = 0
    def __init__(self, z, x):
        self.value: int = Entry.entry_counter
        self.z = z
        self.x = x

        Entry.entry_counter += 1

        ALL_OBJECTS.append(self)

    def resolve(self):
        return str(self)

    def __str__(self):
        return f"e[{self.value}]"

class Exit:
    def __init__(self):
        self.completed = False
        self.z = None
        self.x = None
        self.expr = None

    def resolve(self):
        self.expr.resolve()

    def __str__(self):
        return f"exit = {str(self.expr)}"

ALL_OBJECTS = []