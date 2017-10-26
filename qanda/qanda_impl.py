from qanda import *
from userEntityImpl import *
from questionEntityImpl import *
from answerEntityImpl import *
import abc
import sqlite3
conn = sqlite3.connect( "test.db", isolation_level = None )
c = conn.cursor()

class QandA_Impl(metaclass=abc.ABCMeta):
    def initialize(self):
        """make sure database is empty by deleting all existing rows"""
        c.execute('''DROP TABLE IF EXISTS User''')
        c.execute('''DROP TABLE IF EXISTS Question''')
        c.execute('''DROP TABLE IF EXISTS Answer''')
        c.execute('''DROP TABLE IF EXISTS Vote''')
        userEntityImpl.initialize(self)
        questionEntityImpl.initialize(self)
        answerEntityImpl.initialize(self)
        return

    def user_entity(self):
        """return an object that implements UserEntity"""
        user_entity = userEntityImpl()
        return user_entity

    def question_entity(self):
        """return an object that implements QuestionEntity"""
        question_entity = questionEntityImpl()
        return question_entity

    def answer_entity(self):
        """return an object that implements AnswerEntity"""
        answer_entity = answerEntityImpl()
        return answer_entity