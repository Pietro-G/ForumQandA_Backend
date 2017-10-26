from qanda import *
import abc
import sqlite3
import uuid
conn = sqlite3.connect( "QandA.db", isolation_level = None )
c = conn.cursor()

class questionEntityImpl(metaclass=abc.ABCMeta):
    def initialize(self):
        """create table for this class if necessary"""
        c.execute('''CREATE TABLE IF NOT EXISTS Question (id TEXT, uid TEXT, body TEXT, PRIMARY KEY(id))''')
        c.execute('''DELETE FROM Question''')
        """delete all rows in the table for this class"""
        return

    def get(self, id):
        """return object with matching id"""
        """KeyError exception should be thrown if id not found"""
        c.execute('''SELECT * FROM Question where id = ?''', (id,))
        questionEntry = c.fetchone()
        if questionEntry != None:
            questionObject = Question(questionEntry[0], questionEntry[2])
        else:
            raise KeyError
        return questionEntry

    def get_all(self):
        c.execute("SELECT * FROM Question")
        question_objects = []
        rows = c.fetchall()
        for column in rows:
            question = Question(column[0], column[2])
            question_objects.append(question)
        return question_objects
        """return all objects in an array"""
        """if no user objects are found, returned array should be empty"""

    def delete(self, id):
        """delete object with matching id"""
        """KeyError exception should be thrown if id not found"""
        c.execute("SELECT * from Question where id = ?",(id,))
        questionHit = c.fetchone()
        if questionHit:
            c.execute('''Delete FROM Question WHERE id = ?''', (id,))
            c.execute('''Delete FROM Answer WHERE qid = ?''', (id,))
        else:
            raise KeyError

    def new(self, user_id, text):
        """allow a user to pose a question"""
        """unique question id is returned"""
        """KeyError exception should be thrown if user_id not found"""
        uniqueId = str(uuid.uuid4())
        c.execute('''SELECT count(*) FROM User WHERE id = ?''', (user_id,))
        validUserId = c.fetchone()[0]
        if validUserId >= 1:
            c.execute('''INSERT INTO Question VALUES (?,?,?)''', (uniqueId, user_id, text))
            return uniqueId
        else:
            raise KeyError