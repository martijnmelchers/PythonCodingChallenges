from typing import Type
from operations import *


class OperationFactory:
    def __init__(self):
        self.operations: dict[str, Operation] = {
            "\\": String(),
            "*": Integer(),

            "rot": Rot13(),  #
            "dup": Duplicate(),  #
            "cat": Concat(),  #
            "rev": Reverse(),  #
            "idx": AtIndex(),  #
            "slc": Slice(),  #
            "len": Length(),
            "enl": NewLine(),

            "add": Add(),
            "sub": Subtract(),
            "mul": Multiply(),  #
            "div": Divide(),  #
            "mod": Modular(),  #
            "neg": Negate(),
            "abs": Absolute(),  #
            "inc": Increment(),
            "dec": Decrement(),

            "gto": Goto(),
            "gne": GotoNotEqual(),
            "glt": GotoLess(),
            "gle": GotoLessEqual(),
            "ggt": GotoGreater(),
            "gge": GotoGreaterEqual(),

            "=": DefineVariable(),  #
            "$": ReadVariable(),  #

            "fun": DefineFunction(),  #
            "ret": ReturnFunction(),  #

            ":": DefineLabel(),  #
            ">": ReadLabel()  #
        }

    def get_operation(self, line: str) -> Operation:
        first_char = line[0]
        if first_char in self.operations:
            return self.operations[first_char]

        if line.isdigit():
            return self.operations["*"]

        return self.operations[line]

    
    
