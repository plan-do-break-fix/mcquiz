#!/usr/bin/python3

import sqlite3
from typing import List, Union

SCHEMA = [
    "questionSet ("\
    "  pk INTEGER PRIMARY KEY,"\
    "  name TEXT NOT NULL"
    ");",
    "question ("\
    "  pk INTEGER PRIMARY KEY,"\
    "  fingerprint TEXT NOT NULL,"\
    "  questionSet INTEGER NOT NULL,"\
    "  FOREIGN KEY (questionSet)"\
    "    REFERENCES questionSet (pk)"\
    "    ON DELETE CASCADE"
    ");",
    "quiz ("\
    "  pk INTEGER PRIMARY KEY,"\
    "  questionSet INTEGER NOT NULL,"\
    "  datetime DATETIME NOT NULL,"\
    "  score INTEGER NOT NULL"
    "  FOREIGN KEY (questionSet)"\
    "    REFERENCES questionSet (pk)"\
    "    ON DELETE CASCADE"
    ");",
    "questionHistory ("\
    "  pk INTEGER PRIMARY KEY,"\
    "  question INTEGER NOT NULL,"\
    "  quiz INTEGER NOT NULL,"\
    "  mark INTEGER NOT NULL"\
    "  FOREIGN KEY (question)"\
    "    REFERENCES question (pk)"\
    "    ON DELETE CASCADE,"\
    "  FOREIGN KEY (quiz)"\
    "    REFERENCES quiz (pk)"\
    "    ON DELETE CASCADE"\
    ");"
]

class Interface:

    def __init__(self, db_path):
        self.db = sqlite3.connect(db_path)
        self.c = self.db.cursor()

    def record_quiz_results(self, question_set_pk: int, timestamp: str, score: int, questions: List, marks: List) -> bool:
        if not len(questions) == len(marks):
            raise RuntimeError
        quiz_pk = self.insert_quiz(question_set_pk, timestamp, score)
        for _i, _q in enumerate(questions):
            question_pk = self.question_exists(_q.pk)
            self.insert_question_history(question_pk, quiz_pk, marks[_i])
        self.db.commit()
        return True

    def insert_question_set(self, name: str) -> int:
        self.c.execute("INSERT INTO questionSet (name) VALUES (?)", (name,))
        self.db.commit()
        return self.c.lastrowid

    def insert_question(self, question_set_pk: int, fingerprint: str) -> int:
        self.c.execute("INSERT INTO question (questionSet, fingerprint) VALUES (?,?)",
                       (question_set_pk, fingerprint))
        self.db.commit()
        return self.c.lastrowid

    def insert_quiz(self, question_set_pk: int, timestamp: str, score: int) -> int:
        self.c.execute("INSERT INTO quiz (question_set, datetime, score) VALUES (?, ?, ?)", 
                       (question_set_pk, timestamp, score))
        self.db.commit()
        return self.c.lastrowid

    def insert_question_history(self, question_pk: int, quiz_pk: int, mark: int):
        if mark not in [0,1]:
            raise RuntimeError
        self.c.execute("INSERT INTO questionHistory (question, quiz, mark) VALUES (?, ?, ?)",
                       (question_pk, quiz_pk, mark))
        self.db.commit()
        return self.c.lastrowid

    def question_set_exists(self, question_set: str) -> Union[int, bool]:
        self.c.execute("SELECT pk FROM questionSet WHERE name=?", (question_set,))
        result = self.c.fetchone()
        return result[0] if result else False

    def question_exists(self, fingerprint: str) -> Union[int, bool]:
        self.c.execute("SELECT pk FROM question WHERE fingerprint=?", (fingerprint,))
        result = self.c.fetchone()
        return result[0] if result else False
