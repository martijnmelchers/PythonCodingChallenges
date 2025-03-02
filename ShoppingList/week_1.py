# # Opdracht 1
# ### **Challenge: Grocery List Manager**
#
# #### **Problem Statement**
# Create a **grocery list manager** where users can:
# 1. **Add items** with a quantity. If the item already exists, inform the user and do nothing.
# 2. **Update an existing item’s quantity** in the list.
# 3. **Remove items** from the list.
# 4. **View the list** in a readable format.
# 5. **Exit** the program when done.
#
# #### **Requirements**
# - Store the grocery list in a **dictionary**, where the key is the item name and the value is the quantity.
# - Use a **list** to store menu options and display them dynamically.
# - Keep running until the user chooses to exit.
# - **Input validation**:
#   - Only accept positive integers for quantities.
#   - Prevent empty item names.
#   - Ensure an item exists before updating or removing it.
#
# ---
#
# ### **Example Menu Output**
# ```
# Welcome to the Grocery List Manager!
# Options:
# 1. Add Item
# 2. Update Item Quantity
# 3. Remove Item
# 4. View List
# 5. Exit
# Enter your choice:
# ```
#
# ---
#
# ### **Core Tasks**
# - Implement a function to **display the menu** dynamically based on the list.
# - Implement a function to **add an item**, ensuring it doesn’t already exist.
# - Implement a function to **update an existing item’s quantity**.
# - Implement a function to **remove an item**, ensuring it exists first.
# - Implement a function to **view the grocery list**.
# - Implement a function to **exit the program**.
#
# ---
#
# ### **Extra Challenge (Optional Enhancements)**
# Modify the program to:
# - **Replace the menu list with a dictionary** that maps menu options to functions for a cleaner structure.
# - Allow users to **enter menu names instead of numbers** (e.g., `"Add Item"` instead of `"1"`).
# - Implement **error handling** for invalid inputs.
# - Add an option to **save the grocery list to a file** and **load it on startup**.
# - Allow users to **clear the entire list** with a new menu option.
# - Add an option to **sort the list alphabetically** before displaying.
import os
import sys
from collections.abc import Callable
import re






def main():
    try:
        while True:
            clear()
            print("[🎉] Welcome to your grocery list! Please select an option:")
            print_operations()
            option = parse_option(input("[?] What would you like to do?\n> "))

            if option is None:
                print("[!] Invalid option, select a valid one!")
            else:
                clear()
                try:
                    option()
                except KeyboardInterrupt:
                    print("[-] Operation canceled.")

    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Exiting gracefully...")
        sys.exit(0)  # Exit cleanly
    except SystemExit:
        print("\nSystem exit requested. Shutting down...")
        sys.exit(0)  # Ensure a clean exit


# Operations
def add_item():
    print("[*] Adding item to your list ")

    while (item := input("[?] What item would you like to add?\n> ")) and find_item(item) is not None:
        print("[!] You cannot add an item that is already on your list")

    while not (quantity := input("[?] How many?\n> ")).isdigit() or int(quantity) < 1:
        print("[!] Invalid quantity. Please enter a positive number")

    shopping_list[item] = int(quantity)
    write_shopping_list()
    print("[✔] Item added")


def update_item():
    print("[*] Update item in your list")

    while (item := find_item(input("[?] What item would you like to remove?\n> "))) is None:
        print("[!] Item not on your shopping list!")

    while not (quantity := input("[?] How many?\n> ")).isdigit() or int(quantity) < 1:
        print("[!] Invalid quantity. Please enter a positive number")

    shopping_list[item] = int(quantity)
    write_shopping_list()
    print("[✔] Item updated")


def remove_item():
    print("[*] Remove item from your list")

    while (item := find_item(input("[?] What item would you like to remove?\n> "))) is None:
        print("[!] Item not on your shopping list!")

    del shopping_list[item]
    write_shopping_list()
    print("[✔] Item removed")

def view_list():
    for index, (item, quantity) in enumerate(shopping_list.items()):
        print(f"[{index + 1}] {quantity}x {item} ")

    if len(shopping_list.items()) == 0:
        print("[*] No items on your list")

    input("[>] Press enter to go back to the main menu")

def save_list():
    global has_save
    if has_save:
        remove_list = confirm("Your list is already automatically being saved, would you like to removed your saved list?")
        if remove_list:
            os.remove("shopping_list.txt")
            print("[✔] Saved list removed!")
        else:
            print("[-] Saved list kept!")
    else:
        print("[*] Want to keep your list saved when you exit the program?")
        print("[*] This will save your list in a file which will be remembered until you disable it again.")
        print("[*] Your file will be automatically updated when you update your list.")
        wants_to_save = confirm("Want to save your list?")

        if wants_to_save:
            has_save = True
            write_shopping_list()

def clear_list():
    if confirm("Are you sure you want to clear your list?"):
        shopping_list.clear()
        write_shopping_list()
        print("[✔] Shopping list cleared")
    else:
        print("[-] List not cleared")

def exit_list():
    sys.exit(0)

# Helper functions

def write_shopping_list():
    if has_save:
        save = open(save_name, "w")
        dict_as_string = ""
        for i, (item, quantity) in enumerate(shopping_list.items()):
            dict_as_string += f"{item.replace(':', '\\:')}:{quantity}"
            if i < len(shopping_list) - 1:
                dict_as_string += "\n"

        save.write(dict_as_string)
        save.close()

def read_shopping_list():
    if has_save:
        save = open(save_name, "r")
        read_dict = {}

        for raw_item in save.read().splitlines():
            if not raw_item.strip():
                continue

            try:
                item, quantity = re.split(r'(?<!\\):', raw_item)
                read_dict[item.replace('\\:', ':')] = quantity
            except ValueError:
                print(f"[!] Malformed save: {raw_item}")

        return read_dict

    return {}


def print_operations():
    for i, key in enumerate(operations.keys()):
        print(f"[{i + 1}] {key}")

def parse_option(requested_operation: str) -> Callable[[], None] | None:
    # If we can parse the input as an integer, use it as an index, otherwise we check if the key exists in the dictionary
    if requested_operation.isdigit():
        index = int(requested_operation) - 1
        if index > len(operations_normalized):
            return None

        return list(operations_normalized.values())[index]
    else:
        if normalize(requested_operation) in operations_normalized:
            return operations_normalized[normalize(requested_operation)]

def find_item(item) -> str | None:
    for key in shopping_list.keys():
        if key.lower() == item.lower():
            return key
    return None

def confirm(question: str) -> bool:
    answer = input(f"[?] {question} (Y/N)\n> ")

    if answer.lower() == "y" or answer.lower() == "yes":
        return True
    return False

def clear():
    print('--------------------------------------------------------------------------------------------')

def normalize(string: str) -> str:
    return string.lower().strip()

# Globals
save_name = "shopping_list.txt"
has_save = os.path.exists(save_name)
shopping_list: dict[str, int] = read_shopping_list()
operations = {
    "Add Item": add_item,
    "Update Quantity": update_item,
    "Remove Item": remove_item,
    "List Items": view_list,
    "Save List": save_list,
    "Clear List": clear_list,
    "Exit": exit_list
}
operations_normalized = {key.lower(): value for key, value in operations.items()}
main()