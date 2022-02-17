import sqlite3
from db import Database

db = Database("ovs")

def migrate():
    connection = sqlite3.connect("ovs.db")
    cursor = connection.cursor()
    # roll 1 normal, roll 2 steerer
    cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS Users
                  (id TEXT PRIMARY KEY,
                  email TEXT,
                  passhash TEXT,
                  roll INT,
                  timestamp TIMESTAMP NOT NULL DEFAULT {db.timestamp_now})"""
    )

    cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS Polls
                  (id TEXT PRIMARY KEY,
                  signature TEXT,
                  title TEXT, 
                  opt1 TEXT, 
                  opt2 TEXT, 
                  opt3 TEXT, 
                  opt4 TEXT, 
                  opt5 TEXT, 
                  active INT,
                  closing_date TEXT,
                  timestamp TIMESTAMP NOT NULL DEFAULT {db.timestamp_now})"""
    )

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS Approvals
                  (id TEXT PRIMARY KEY,
                  poll_id TEXT, 
                  passhash TEXT)"""
    )

#Proof user has voted, so they cant vote again
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS VoteCheck
                  (id TEXT PRIMARY KEY,
                  poll_id TEXT, 
                  user_id TEXT)"""
    )

#Hash of users email and password, so anon vote that can be counted
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS Vote
                  (id TEXT PRIMARY KEY,
                  poll_id TEXT, 
                  vote_opt INT)"""
    )

    connection.commit()
    connection.close()
    print("database built!")
