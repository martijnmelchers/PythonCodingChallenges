import decimal
import os.path
from collections.abc import Callable
from decimal import Decimal


class UserAccount:
    def __init__(self, pin: str, balance: float):
        self.pin = pin
        self.balance: float = balance

    def deposit(self, amount: float):
        self.balance += amount
        self.save()

    def withdraw(self, amount: float):
        self.balance -= amount
        self.save()

    def has_balance(self, amount: float):
        pass

    def save(self):
        with open(f"{self.pin}.txt", "w") as balance:
            balance.write(self.balance.__str__())




class BankSystem:
    logged_out_menu: dict[str, Callable]
    logged_in_menu: dict[str, Callable]

    def __init__(self):
        self.account: UserAccount | None = None
        self.logged_out_menu = {
            "Login": self.login,
            "Register": self.register
        }
        self.logged_in_menu = {
            "Deposit": self.deposit,
            "Transfer": self.transfer,
            "Logout": self.logout
        }

    def start(self):
        while True:
            if self.account is None:
                self.print_menu(self.logged_out_menu)
                self.select_menu_option(self.logged_out_menu)
            else:
                self.print_menu(self.logged_in_menu)
                self.select_menu_option(self.logged_in_menu)

    @staticmethod
    def print_menu(menu: dict[str, Callable]):
        for i, key in enumerate(menu.keys()):
            print(f"[{i + 1}] {key}")

    def login(self):
        pin = input("Enter your 4-digit pin:\n > ")

        if not pin.isdigit() or len(pin) != 4:
            print("Invalid pin, please enter a 4-digit pin.")
            return

        if not os.path.exists(f"{pin}.txt"):
            print("Pin does exist")
            return

        with open(f"{pin}.txt", "r") as balance:
            self.account = UserAccount(pin, float(balance.read()))
            print("Successfully logged in!")

    def register(self):
        while (((pin := input("Enter your 4-digit pin:\n > ")).isdigit() is False
               or len(pin) != 4)
               or os.path.exists(f"{pin}.txt")):
            print("Invalid pin, please enter a 4-digit pin.")

        with open(f"{pin}.txt", "w") as balance:
            balance.write("100")
            self.account = UserAccount(pin, 100)

    def deposit(self):
        amount = input("How much do you want to deposit?\n> ")

        if not amount.isdecimal() or float(amount) < 0:
            print("Please deposit a positive amount")
            return

        self.account.deposit(float(amount))



    def transfer(self):
        pass

    def logout(self):
        print("Goodbye!")
        self.account = None

    @staticmethod
    def select_menu_option(menu: dict[str, Callable]):
        user_input = input(f"Select an option (1-{len(menu)}):\n> ")

        if not user_input.isdigit() or int(user_input) < 1 or int(user_input) > len(menu):
            print("Invalid option!")
            return

        list(menu.values())[int(user_input) - 1]()






# account = UserAccount(5.34)
#
# print(account.balance)
# account.withdraw(5)
#
# print(account.balance)
#
# print("a".__len__())

BankSystem().start()
