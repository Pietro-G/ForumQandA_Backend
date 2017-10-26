from qanda import *
import abc
import sqlite3
import uuid
conn = sqlite3.connect("QandA.db", isolation_level = None )
c = conn.cursor()
c2 = conn.cursor()

class answerEntityImpl(metaclass=abc.ABCMeta):
    def initialize(self):
        """create table for this class if necessary"""
        c.execute('''CREATE TABLE IF NOT EXISTS Answer (id TEXT, qid TEXT, uid TEXT, body TEXT, PRIMARY KEY(id))''')
        c.execute('''CREATE TABLE IF NOT EXISTS Vote (uid TEXT, aid TEXT, vote INTEGER, PRIMARY KEY (uid, aid))''')
        c.execute('''DELETE FROM Answer''')
        c.execute('''DELETE FROM Vote''')
        """delete all rows in the table for this class"""
        return

    def get(self, id):
        """return object with matching id"""
        """KeyError exception should be thrown if id not found"""
        c.execute('''SELECT * FROM Answer where id = ?''', (id,))
        answerRow = c.fetchone()
        if answerRow is None:
            raise KeyError
        else:
            c2.execute('''SELECT count(*) FROM Vote WHERE aid = ? AND vote = 1''', (id,))
            upVote = c2.fetchone()[0]
            c2.execute('''SELECT count(*) FROM Vote WHERE aid = ? AND vote = -1''', (id,))
            downVote = c2.fetchone()[0]
            answerObject = Answer(id, answerRow[3], upVote, downVote)
        return answerObject

    def get_all(self):
        c.execute('''SELECT * FROM Answer''')
        answerEntries = []
        answerRows = c.fetchall()
        for column in answerRows:
            c2.execute('''SELECT count(*) FROM Vote WHERE aid = ? AND vote = 1''', (column[0],))
            upVote = c2.fetchone()[0]
            c2.execute('''SELECT count(*) FROM Vote WHERE aid = ? AND vote = -1''', (column[0],))
            downVote = c2.fetchone()[0]
            answerObject = Answer(column[0], column[3], upVote, downVote)
            answerEntries.append(answerObject)

        return answerEntries

    def delete(self, id):
        """delete object with matching id"""
        """KeyError exception should be thrown if id not found"""
        c.execute('''SELECT * FROM Answer WHERE id = ?''', (id,))
        entryToDelete = c.fetchone()
        if entryToDelete is not None:
            c.execute('''DELETE From Answer WHERE id = ?''', (id,))
        else:
            raise KeyError
        return

    def new(self, user_id, question_id, text):
        """allow a user to answer a question"""
        """unique answer id is returned"""
        """KeyError exception should be thrown if user_id or question_id not found"""
        c.execute('''SELECT count(*) FROM User WHERE id = ?''', (user_id,))
        userHit = c.fetchone()[0]
        c.execute('''SELECT count(*) FROM Question WHERE id = ?''', (question_id,))
        questionHit = c.fetchone()[0]
        if userHit == 1 and questionHit == 1:
            uniqueId = str(uuid.uuid4())
            c.execute('''INSERT INTO Answer("id", "uid", "qid", "body") VALUES (?,?,?,?)''', (uniqueId, user_id, question_id, text))
            return uniqueId
        else:
            raise KeyError


    def get_answers(self, question_id):
        """find all answers to a question"""
        """answers are returned as an array of Answer objects"""
        """KeyError exception should be thrown if question_id not found"""
        allAnswers = []
        c.execute('''SELECT * FROM Answer WHERE qid = ?''', (question_id,))
        answersFound = c.fetchall()
        if answersFound is None:
            raise KeyError
        else:
            for column in answersFound:
                answerObject = self.get(column[0])
                allAnswers.append(answerObject)
            return allAnswers

    def vote(self, user_id, answer_id, vote):
        """allow a user to vote on a question; vote is of class Vote"""
        """up and down votes are returned as a pair"""
        """KeyError exception should be thrown if user_id or answer_id not found"""
        voteValue = vote.value
        upVote = 0
        downVote = 0
        voteTupple = (upVote,downVote)
        if (voteValue > 0):
            upVote += voteValue
            voteTupple = (upVote,downVote)
        else:
            downVote += voteValue
            voteTupple = (upVote,downVote)
        c.execute('''SELECT count(*) FROM User WHERE id = ?''', (user_id,))
        usersFound = c.fetchone()[0]
        c.execute('''SELECT count(*) FROM Answer WHERE id = ?''', (answer_id,))
        answersFound = c.fetchone()[0]
        if usersFound != 0 and answersFound != 0:
            uniqueId = str(uuid.uuid4())
            c.execute('''INSERT INTO Vote(uid, aid, vote) VALUES (?, ?, ?)''', (user_id, answer_id, voteValue))
            return voteTupple
        else:
            raise KeyError
