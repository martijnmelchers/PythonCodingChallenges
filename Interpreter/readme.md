# Pyterpreter

## Overview
Pyterpreter is a custom interpreter designed to read and execute commands from a file. The interpreter processes operations as described below, utilizing a stack-based approach.

## Technical Requirements
- **Stack-Based Execution:** Data must be processed and stored using a stack.
- **Object-Oriented Design:**
  - Implement a class to manage the stack and relevant variables.
  - Use an abstract class to define operations, with child classes implementing specific operations (e.g., ROT13 transformation).
- **Code Organization:**
  - Operations, stack handling, and file parsing must be implemented in separate files.
- **HTTP File Handling:**
  - The interpreter fetches files from a provided URL.
- **Constraints:**
  - No external libraries should be used.
  - No global variables should be used, except at the program’s start.
- **Error Handling:** The program must handle errors and exceptions gracefully.

### Optional Technical Enhancements
- **Factory Pattern:**
  - Implement a factory to create operations dynamically.
  - Maintain a dictionary mapping operation names to their respective classes.
  - Example usage: `factory.get_operation("rot")` returns the ROT13 operation class.
- **Logging:**
  - Implement a logger for debugging.
  - Log format: `{operation} > {input} -> {output}` (e.g., `rot > "hello" -> "uryyb"`).
  - Enable logging via a debug flag.
- **Unit Testing:**
  - Implement unit tests to verify operations.
- **Command-Line Interface (CLI):**
  - Support command-line arguments for enabling debugging and logging.

## Functional Requirements
- **File Reading:**
  - The interpreter starts with the URL: `https://interpreter.goofyincorporated.com/start.txt`.
  - Files reference subsequent URLs using the base path: `https://interpreter.goofyincorporated.com/`.
- **Parsing and Execution:**
  - The interpreter parses the file and executes operations sequentially.
- **Supported Operations:**
  - Detailed below in the **Operations** section.

### Optional Functional Enhancements
- **Logging Operations:**
  - Log operations performed when debug mode is enabled.
- **CLI Enhancements:**
  - Support CLI flags for enabling logging and debug mode.

## Stack Implementation
The interpreter uses a stack to manage data. Operations interact with this stack by pushing, popping, and modifying values.

Example:
```python
class StackData:
    def __init__(self):
        self.stack: list[str] = []
        self.variables: dict[str, str] = {}
        self.labels: dict[str, int] = {}
        self.functions: list[int] = []
        self.position: int = 0
        self.line: str = ""

    def get_and_pop(self) -> str:
        value = self.stack.pop()
        return value
```

### Stack Behavior Example:
- Given a stack: `["hello", "world"]`
- Popping twice results in:
  ```python
  value_1 = stack.pop() # "world"
  value_2 = stack.pop() # "hello"
  concat = value_2 + value_1  # "helloworld"
  ```

## Operations
### String Operations
- `\` - Define a string and push it to the stack.
- `rot` - Apply ROT13 to the last string in the stack.
- `cat` - Concatenate the last two strings.
- `rev` - Reverse the last string.
- `idx` - Retrieve a character at a given index from a string.
- `slc` - Extract a substring using start and end indices.
- `len` - Get the length of a string.
- `enl` - Append a newline to the last string.

### Number Operations
- Numbers are pushed directly to the stack.
- `add` - Add the last two numbers.
- `sub` - Subtract the last two numbers.
- `mul` - Multiply the last two numbers.
- `div` - Divide the last two numbers.
- `mod` - Compute the modulus.
- `neg` - Negate the last number.
- `abs` - Compute the absolute value.
- `inc` - Increment the last number.
- `dec` - Decrement the last number.

### Jump Operations
Input order is always: `value1, value2, line_number`. (Values only apply to comparison operations.)
- `gto` - Jump to a specific line number.
- `gne` - Compare two values; jump if they are not equal.
- `glt` - Compare two values; jump if the first is less than the second.
- `gle` - Compare two values; jump if the first is less than or equal to the second.
- `ggt` - Compare two values; jump if the first is greater than the second.
- `gge` - Compare two values; jump if the first is greater than or equal to the second.

### Function Operations
- `fun` - Store the current line and jump to the function’s line.
- `ren` - Return from a function.

### Label Operations
Tip: You should evaluate labels before you execute the rest of the operations, so you can jump to them later.

- `:` - Define a label, storing the current line number.
- `>` - Push a label’s line number onto the stack.

### Variable Operations
- `={name}` - Store the last stack value as a variable.
- `${name}` - Push the variable’s value onto the stack.

### Control Operations
- `end` - Terminate execution and return the last stack value.