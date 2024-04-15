import baseball_db as db

def get_int():
    """
        Continuously prompts the user to enter an integer until a valid integer is provided.
        Returns:
            int: The integer entered by the user.
    """
    while True:
        try:
            response = int(input("Enter an integer: "))
            return response
        except ValueError:
            print("invalid")

def view():
    """
        Displays a formatted table of players and their statistics from the database.
    """
    print(f'{"name"}{"wins"}{"losses"}{"ties"}{"games"}')
    print('--------------------------------------------------')
    for player in db.players:
        print(f'{player}')

def add():
    """
        Adds a new player to the database based on user input for name, wins, losses, and ties.
    """
    name = input("name: ")
    wins = input("wins: ")
    losses = input("losses: ")
    ties = input("ties: ")
    db.Add(name, wins, losses, ties)
    print(f"{name} was added succesfully")

def update():
    """
        Updates an existing player's statistics in the database based on user input.
    """
    name = input("name: ")
    wins = input("wins: ")
    losses = input("losses: ")
    ties = input("ties: ")
    db.Update(name, wins, losses, ties)
    print(f"{name} was updated")

def delete():
    """
        Deletes a player from the database based on user input for the player's name.
    """
    name = input("name: ")
    db.Delete(name)
    print(f"{name} was deleted")
