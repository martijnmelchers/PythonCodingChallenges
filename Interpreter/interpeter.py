from urllib.request import Request, urlopen

from Interpreter.operation_factory import OperationFactory
from Interpreter.stack_data import StackData


class Interpreter:
    def __init__(self, path: str, factory: OperationFactory):
        self.path = path
        self.data = StackData()
        self.lines: list[str] = []
        self.finished = False
        self.operation_factory = factory
    
    # starts the interpreter, outputs the solution
    def execute(self) -> (bool, str):
        if self.path.startswith("https://"):
            request = Request(f"{self.path}")
            request.add_header("User-Agent",
                               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36")

            with urlopen(request) as content:
                self.lines = content.read().decode('utf-8').splitlines()
        else:
            with open(self.path, "r") as file:
                self.lines = file.read().splitlines()
            
            
        self.read_labels()
        
        return self.finished, self.interpret()
                
    def read_labels(self):
        while self.data.position < len(self.lines):
            self.data.line = self.lines[self.data.position]
            if self.data.line[0] == ":":
                operation = self.operation_factory.get_operation(self.data.line)
                operation.execute(self.data)

            self.data.position += 1

        self.data.position = 0

    def interpret(self) -> str:
        while self.data.position < len(self.lines):
            self.data.line = self.lines[self.data.position]

            if self.data.line == "end":
                return self.data.stack[-1]

            operation = self.operation_factory.get_operation(self.data.line)
            operation.execute(self.data)

            self.data.position += 1
        return self.data.stack[-1]
        

    


