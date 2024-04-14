import baseball_business as business

def main():
    """
        Displays the Player Manager's command menu.
    """
    print("Player Manager")
    print()
    print("COMMAND MENU")
    print("view - View players")
    print("add - Add a player")
    print("update - Update a player")
    print("del - Delete a player")
    print("exit - Exit program")

while True:
    """
        Runs the Player Manager program, handling user commands.
        Displays the command menu and processes user input until the user chooses to exit.
    """
    command = input("command: ").lower()
    if command == "view":
        business.view()
    elif command == "add":
        business.add()
    elif command == "update":
        business.update()
    elif command == "del":
        business.delete()
    elif command == "exit":
        print("Bye!")
        break
    else:
        print("Invalid")

