import sqlite3
import pandas as pd

# Load cleaned CSV
try:
    df = pd.read_csv("leaders_for_wins_cleaned.csv")

    # Connect to SQLite database (or create it if it doesn't exist)
    with sqlite3.connect("baseball_leaders.db") as conn:
        cursor = conn.cursor()

        # Drop the table if it exists
        cursor.execute("DROP TABLE IF EXISTS leaders_for_wins")

        # Create the table with proper schema
        cursor.execute("""
            CREATE TABLE leaders_for_wins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                year INTEGER,
                league TEXT,
                player TEXT,
                wins REAL,
                team TEXT
            )
        """)

        # Loop through df and insert data into the database
        for __, row in df.iterrows():
            cursor.execute("""
                INSERT INTO leaders_for_wins (year, league, player, wins, team)
                VALUES (?, ?, ?, ?, ?)
            """, (row['Year'], row['League'], row['Player'], row['Wins'], row['Team']))

        # Commit the changes to the database
        conn.commit()
        print("Loaded leaders_for_wins_cleaned.csv into the database successfully.")

except (sqlite3.Error, pd.errors.EmptyDataError) as e:
    print(f"An error occurred: {e}")