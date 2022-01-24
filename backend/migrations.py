import sqlite3


def migrate():
    connection = sqlite3.connect("ovs.db")
    cursor = connection.cursor()
    # roll 1 normal, roll 2 steerer
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS Users
                  (id TEXT PRIMARY KEY,
                  roll INT,
                  timestamp TEXT)"""
    )

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS Polls
                  (id TEXT PRIMARY KEY,
                  title TEXT, 
                  opt1 TEXT, 
                  opt2 TEXT, 
                  opt3 TEXT, 
                  opt4 TEXT, 
                  opt5 TEXT, 
                  active INT,
                  closing_date TEXT,
                  timestamp TEXT)"""
    )

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS Approvals
                  (id TEXT PRIMARY KEY,
                  poll_id TEXT, 
                  user_id TEXT)"""
    )

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS Votes
                  (id TEXT PRIMARY KEY,
                  poll_id TEXT, 
                  user_id TEXT, 
                  vote_opt INT,
                  timestamp TEXT)"""
    )


    connection.commit()
    connection.close()
    print("database built!")
