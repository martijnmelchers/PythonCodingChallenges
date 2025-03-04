from abc import ABC, abstractmethod
from typing import Type


class StackData:
    def __init__(self):
        self.stack: [str] = []
        self.variables: dict[str, str] = {}
        self.labels: dict[str, int] = {}
        self.functions: [int] = []
        self.position: int = 0
        self.line: str = ""

    def get_and_pop(self) -> str:
        value = self.stack[-1]
        self.stack.pop()

        return value

    def __str__(self):
        return f"StackData({self.stack}, {self.variables}, {self.labels}, {self.functions}, {self.position}, {self.line})"

class Operation(ABC):

    @abstractmethod
    def execute(self, data: StackData):
        pass


class Rot13(Operation):

    def execute(self, data: StackData):
        rot13 = str.maketrans('ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz',
                              'NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm')
        value = data.get_and_pop().translate(rot13)
        data.stack.append(value)

class Duplicate(Operation):
    def execute(self, data: StackData):
        data.stack.append(data.stack[-1])

class Concat(Operation):
    def execute(self, data: StackData):
        part_1 = data.get_and_pop()
        part_2 = data.get_and_pop()

        data.stack.append(part_2 + part_1)

class AtIndex(Operation):
    def execute(self, data: StackData):
        index = int(data.get_and_pop())
        string = data.get_and_pop()

        print(string)
        print(index)

        data.stack.append(string[index])

class Reverse(Operation):
    def execute(self, data: StackData):
        string = data.get_and_pop()
        data.stack.append(string[::-1])

class SetVariable(Operation):
    def execute(self, data: StackData):
        content = data.get_and_pop()
        data.variables[data.line[1:]] = content

class ReadVariable(Operation):
    def execute(self, data: StackData):
        data.stack.append(data.variables[data.line[1:]])

class String(Operation):

    def execute(self, data: StackData):
        data.stack.append(data.line[1:])

class Integer(Operation):

    def execute(self, data: StackData):
        data.stack.append(data.line)


operations: dict[str, Type[Operation]] = {
    "\\": String,
    "=": SetVariable,
    "$": ReadVariable,
    "*": Integer,
    "rot": Rot13,
    "dup": Duplicate,
    "cat": Concat,
    "rev": Reverse,
    "idx": AtIndex
}

def find_operation(line: str) -> Operation:
    first_char = line[0]
    if first_char in operations:
        return operations[first_char]()

    if line.isdigit():
        return operations["*"]()

    return operations[line]()


with open("start.txt", "r") as file:
    stack_data = StackData()

    lines = file.read().splitlines()
    while stack_data.position < len(lines):
        stack_data.line = lines[stack_data.position]
        operation = find_operation(stack_data.line)

        operation.execute(stack_data)

        stack_data.position += 1
        print(stack_data)

    print(stack_data.stack[-1])
    print(stack_data)

