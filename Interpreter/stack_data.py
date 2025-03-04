class StackData:
    def __init__(self):
        self.stack: list[str] = []
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