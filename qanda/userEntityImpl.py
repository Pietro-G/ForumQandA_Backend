from qanda import *
import abc
import sqlite3
import uuid
conn = sqlite3.connect( "QandA.db", isolation_level = None )
c = conn.cursor()

class userEntityImpl(metaclass=abc.ABCMeta):
    def initialize(self):
        """create table for this class if necessary"""
        """delete all rows in the table for this class"""
        c.execute('''CREATE TABLE IF NOT EXISTS User (id TEXT, email TEXT, passhash TEXT, PRIMARY KEY(email))''')
        c.execute('''DELETE FROM User''')
        return

    def get(self, id):
        """return object with matching id"""
        """KeyError exception should be thrown if id not found"""
        c.execute('''SELECT * FROM User where id = ?''', (id,))
        userEntry = c.fetchall()
        if userEntry != None:
            userObject = Question(userEntry[0], userEntry[2])
        else:
            raise KeyError
        return userObject

    def get_all(self):
        """return all objects in an array"""
        """if no user objects are found, returned array should be empty"""
        c.execute("SELECT * FROM User")
        userEntries = []
        rows = c.fetchall()
        for column in rows:
            user = User(column[0], column[1], column[2])
            userEntries.append(user)
        return userEntries

    def delete(self, id):
        """delete object with matching id"""
        """KeyError exception should be thrown if id not found"""
        try:
            c.execute('''Delete FROM User WHERE id = ?''', (id,))
        except KeyError:
            return

    def new(self, email, passhash=None):
        """create a new instance in db using the given parameters"""
        """unique user id is returned"""
        """if email already exists, KeyError exception will be thrown"""
        c.execute('''SELECT count(*) FROM User WHERE email = ?''', (email,))
        duplicateHit = c.fetchone()[0]
        if duplicateHit != 1:
            uniqueId = str(uuid.uuid4())
            c.execute('''INSERT INTO User VALUES (?,?,?)''', (uniqueId, email, passhash))
            return uniqueId
        else:
            raise KeyError