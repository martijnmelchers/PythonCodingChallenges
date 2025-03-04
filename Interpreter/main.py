from Interpreter.interpeter import Interpreter
from Interpreter.operation_factory import OperationFactory


def main():
    solved = False
    base_url = "" # https://interpreter.goofyincorporated.com/
    current_solution = "start.txt"
    factory = OperationFactory()

    while not solved:
        interpreter = Interpreter(f"{base_url}{current_solution}", factory)
        finished, solution = interpreter.execute()
        print(f"Found solution: {solution}, finished: {finished}")
        current_solution = solution
        solved = True


if __name__ == "__main__":
    main()