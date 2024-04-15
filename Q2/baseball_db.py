import sqlite3

conn = sqlite3.connect('player_db.sqlite')
c = conn.cursor()

def view():
    """
        Retrieves a list of players from the database, sorted by the number of wins they have.
        Returns:
            list of tuples: A list containing player information, including their name, wins, losses, and ties.
    """
    return list(c.execute('''SELECT * FROM Player ORDER BY wins DESC;'''))
def Add(name: str, wins: int,losses: int,ties:int):
    """
        Adds a new player to the database with their name, win count, loss count, and tie count.
        Args:
            name (str): The name of the player.
            wins (int): The number of wins the player has.
            losses (int): The number of losses the player has.
            ties (int): The number of ties the player has.
    """
    c.execute(f'''INSERT INTO Player VALUES (NULL, "{name}", "{wins}", "{losses}",{ties});''')
def Update(name: str, wins: int,losses: int,ties:int):
    """
        Updates an existing player's record in the database with new win, loss, and tie counts.
        Args:
            name (str): The name of the player to update.
            wins (int): The new number of wins for the player.
            losses (int): The new number of losses for the player.
            ties (int): The new number of ties for the player.
    """
    c.execute (f'''UPDATE Player SET wins = "{wins}", losses = "{losses}", ties = "{ties}" WHERE name = "{name}";''')
def Delete(name: str):
    """
        Deletes a player's record from the database based on their name.
        Args:
            name (str): The name of the player to delete.
    """
    c.execute(f'''DELETE FROM Player WHERE name = "{name}";''')
    conn.commit()

