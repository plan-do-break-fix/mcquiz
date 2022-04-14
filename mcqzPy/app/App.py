#!/usr/bin/python3

from datetime import datetime
import os
from random import sample
from typing import List

from Components import Question, Quiz, ViewParams
from Parser import Parser

from Records import Interface
from Views import TerminalView




class App:

    def __init__(self) -> None:
        self.bank = []
        _path = f"{os.path.expanduser('~')}/.mcqzPy"
        if not os.path.exists(_path):
            os.makedir(_path)
        self.records = Interface(f"{_path}/history.sqlite3.db")


    def load_question_set(self, fpath: str) -> List[Question]:
        q_set_name = fpath.split("/")[-1][:-5]          # drop '.yaml' from file name
        self.q_set = self.records.question_set_exists(q_set_name)
        if not self.q_set:
            self.q_set = self.records.insert_question_set(q_set_name)
        parser, output = Parser(), []
        for _qdict in parser.read_qfile(fpath):
            normal = parser.normalize_qdict(_qdict)
            q_fingerprint = parser.fingerprint(normal)
            q_pk = self.records.question_exists(q_fingerprint)
            if not q_pk:
                q_pk = self.records.insert_question(self.q_set, q_fingerprint)
            normal["pk"] = q_pk
            _q = parser.prepare_question(normal, parser.question_type(normal))
            output.append(_q)
        return output

    def pick(self, count: int) -> List[Question]:
        if count > len(self.bank):
            self.view.error("There are not enough questions in the question bank.")
            raise RuntimeError()
        return sample(self.bank, k=count)
 
    def quiz(self, count: int, max_score: int):
        view = TerminalView.View()
        qz = Quiz(self.pick(count), view)
        timestamp = datetime.now().strptime()    ## TODO
        result = qz.run()
        self.records.record_quiz_results(self.q_set, timestamp, qz.score, qz.questions, qz.marks)

    ##################
    '''
    def begin(self, qs: List[Question], vp: ViewParams) -> None:
        qz = Quiz(qs, TerminalView(vp))
        result = qz.run()
    '''

if __name__ == "__main__":
    #params = QuizParams(20, 1000)
    app, view = App(), TerminalView.View()
    app.load_questions("")
    qz = Quiz(app.pick(20), view)
    qz.run()