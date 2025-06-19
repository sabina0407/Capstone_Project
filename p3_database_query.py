import sqlite3

# Get the database connection 
def connection():
    try:
        conn = sqlite3.connect('baseball_leaders.db')
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None
    
# Display the CLI menu for user interaction
def menu():
    print("\nChoose a Query:")
    print("1. Top leaders by year")
    print("2. Players with wins greater than X")
    print("3. Performance by player name")
    print("4. Players from a specific team")
    print("5. Exit")

# Function to show all leaders for a specific year
def show_leaders_by_year(conn):
    try:
        year = input("Enter the year: ").strip()
        cursor = conn.cursor()
        cursor.execute("SELECT player, team, league, wins FROM leaders_for_wins WHERE year = ?", (year,))
        results = cursor.fetchall()
        if results:
            print(f"\nTop leaders for {year}:")
            for row in results:
                print(f"Player: {row[0]}, Team: {row[1]}, League: {row[2]}, Wins: {row[3]}")
        else:
            print("No data found for this year.")
    except Exception as e:
        print(f"Error fetching leaders by year: {e}")

# function to find players with wins greater than a specified number
def players_above_wins(conn):
    try:
        wins = float(input("Enter the minimum number of wins: ").strip())
        cursor = conn.cursor()
        cursor.execute("SELECT year, player, wins, team, league FROM leaders_for_wins WHERE wins > ? ORDER BY wins DESC", (wins,))
        results = cursor.fetchall()
        if results:
            print(f"\nPlayers with more than {wins} wins:")
            for row in results:
                print(f"Year: {row[0]}, Player: {row[1]}, Wins: {row[2]}, Team: {row[3]}, League: {row[4]}")
        else:
            print("No players found with more than that many wins.")
    except Exception as e:
        print(f"Error fetching players above wins: {e}")

# Function to search for a player's performance by name
def search_player(conn):
    try:
        player_name = input("Enter the player's name: ").strip()
        cursor = conn.cursor()
        cursor.execute("SELECT year, player, wins, team, league FROM leaders_for_wins WHERE player LIKE ? ORDER BY year DESC", (f"%{player_name}%",))
        results = cursor.fetchall()
        if results:
            print(f"\nPerformance for {player_name}:")
            for row in results:
                print(f"Year: {row[0]}, Player: {row[1]}, Wins: {row[2]}, Team: {row[3]}, League: {row[4]}")
        else:
            print("No performance data found for this player.")
    except Exception as e:
        print(f"Error fetching performance by player name: {e}")

# Function to find players from a specific team
def players_from_team(conn):
    try:
        team_name = input("Enter the team name: ").strip()
        cursor = conn.cursor()
        cursor.execute("SELECT year, player, wins, team, league FROM leaders_for_wins WHERE team LIKE ? ORDER BY year DESC", (f"%{team_name}%",))
        results = cursor.fetchall()
        if results:
            print(f"\nPlayers from {team_name}:")
            for row in results:
                print(f"Year: {row[0]}, Player: {row[1]}, Wins: {row[2]}, Team: {row[3]}, League: {row[4]}")
        else:
            print("No players found from this team.")
    except Exception as e:
        print(f"Error fetching players from team: {e}")

# Main function to run the CLI 
def main():
    conn = connection()
    if not conn:
        return

    while True:
        menu()
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            show_leaders_by_year(conn)
        elif choice == '2':
            players_above_wins(conn)
        elif choice == '3':
            search_player(conn)
        elif choice == '4':
            players_from_team(conn)
        elif choice == '5':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

    conn.close()

# Run the program
if __name__ == "__main__":
    main()