from abc import ABC, abstractmethod
from Interpreter.stack_data import StackData

class Operation(ABC):
    @abstractmethod
    def execute(self, data: StackData):
        pass

# String Operations

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

        data.stack.append(string[index])

class Reverse(Operation):
    def execute(self, data: StackData):
        string = data.get_and_pop()
        data.stack.append(string[::-1])

class Length(Operation):
    def execute(self, data: StackData):
        value = data.get_and_pop()
        data.stack.append(str(len(value)))

class Slice(Operation):
    def execute(self, data: StackData):
        start = int(data.get_and_pop())
        end = int(data.get_and_pop())

        value = data.get_and_pop()

        data.stack.append(value[slice(start, end)])

class NewLine(Operation):
    def execute(self, data: StackData):
        value = data.get_and_pop()
        value += "\n"

        data.stack.append(value)
        
# Integer Operations

class Add(Operation):
    def execute(self, data: StackData):
        value_1 = int(data.get_and_pop())
        value_2 = int(data.get_and_pop())
        
        data.stack.append(str(value_2 + value_1))
    
class Subtract(Operation):
    def execute(self, data: StackData):
        value_1 = int(data.get_and_pop())
        value_2 = int(data.get_and_pop())
        
        data.stack.append(str(value_2 - value_1))
    
class Multiply(Operation):
    def execute(self, data: StackData):
        value_1 = int(data.get_and_pop())
        value_2 = int(data.get_and_pop())
        
        data.stack.append(str(value_2 * value_1))

class Divide(Operation):
    def execute(self, data: StackData):
        value_1 = int(data.get_and_pop())
        value_2 = int(data.get_and_pop())
        
        data.stack.append(str(value_2 // value_1))

class Modular(Operation):
    def execute(self, data: StackData):
        value_1 = int(data.get_and_pop())
        value_2 = int(data.get_and_pop())
        
        data.stack.append(str(value_2 % value_1))
    
class Negate(Operation):
    def execute(self, data: StackData):
        value = int(data.get_and_pop())
        data.stack.append(str(-value))
    
class Absolute(Operation):
    def execute(self, data: StackData):
        value = int(data.get_and_pop())
        data.stack.append(str(abs(value)))
    
class Increment(Operation):
    def execute(self, data: StackData):
        value = int(data.get_and_pop())
        data.stack.append(str(value + 1))
    
class Decrement(Operation):
    def execute(self, data: StackData):
        value = int(data.get_and_pop())
        data.stack.append(str(value - 1))

# Jumps

class Goto(Operation):
    def execute(self, data: StackData):
        line = int(data.get_and_pop())
        data.position = line

class GotoNotEqual(Operation):
    def execute(self, data: StackData):
        line = int(data.get_and_pop())
        value_1 = data.get_and_pop()
        value_2 = data.get_and_pop()
        
        if value_2 != value_1:
            data.position = line
    
class GotoLess(Operation):
    def execute(self, data: StackData):
        line = int(data.get_and_pop())
        value_1 = int(data.get_and_pop())
        value_2 = int(data.get_and_pop())
        
        if value_2 < value_1:
            data.position = line
    
class GotoLessEqual(Operation):
    def execute(self, data: StackData):
        line = int(data.get_and_pop())
        value_1 = int(data.get_and_pop())
        value_2 = int(data.get_and_pop())
        
        if value_2 <= value_1:
            data.position = line

class GotoGreater(Operation):
    def execute(self, data: StackData):
        line = int(data.get_and_pop())
        value_1 = int(data.get_and_pop())
        value_2 = int(data.get_and_pop())
        
        if value_2 > value_1:
            data.position = line
    
class GotoGreaterEqual(Operation):
    def execute(self, data: StackData):
        line = int(data.get_and_pop())
        value_1 = int(data.get_and_pop())
        value_2 = int(data.get_and_pop())
        
        if value_2 >= value_1:
            data.position = line
# Functions

class DefineFunction(Operation):
    def execute(self, data: StackData):
        data.functions.append(data.position)

        data.position = int(data.get_and_pop())

class ReturnFunction(Operation):
    def execute(self, data: StackData):
        line = data.functions[-1]
        data.functions.pop()

        data.position = line

# Variables

class DefineVariable(Operation):
    def execute(self, data: StackData):
        content = data.get_and_pop()
        data.variables[data.line[1:]] = content

class ReadVariable(Operation):
    def execute(self, data: StackData):
        data.stack.append(data.variables[data.line[1:]])

# Labels

class DefineLabel(Operation):
    def execute(self, data: StackData):
        data.labels[data.line[1:]] = data.position

class ReadLabel(Operation):
    def execute(self, data: StackData):
        data.stack.append(str(data.labels[data.line[1:]]))

# Values

class String(Operation):

    def execute(self, data: StackData):
        data.stack.append(data.line[1:])

class Integer(Operation):

    def execute(self, data: StackData):
        data.stack.append(data.line)