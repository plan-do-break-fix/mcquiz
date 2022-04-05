#!/usr/bin/python3

from random import sample
from typing import List

from Components import Question, Quiz, ViewParams
from Parser import Parser

from Views import TerminalView




class App:

    def __init__(self) -> None:
        self.bank = []

    def load_questions(self, fpath: str) -> List[Question]:
        parser, output = Parser(), []
        for _qdict in parser.read_qfile(fpath):
            _normal = parser.normalize_qdict(_qdict)
            _q = parser.prepare_question(_normal, parser.question_type(_normal))
            output.append(_q)
        return output


    def pick(self, count: int) -> List[Question]:
        if count > len(self.bank):
            self.view.error("There are not enough questions in the question bank.")
            raise RuntimeError()
        return sample(self.bank, k=count)
 
    ##################
    '''
    def begin(self, qs: List[Question], vp: ViewParams) -> None:
        qz = Quiz(qs, TerminalView(vp))
        result = qz.run()
    '''

if __name__ == "__main__":
    #params = QuizParams(20, 1000)
    app, view = App(), TerminalView.View()
    app.load_questions("/home/jswan/mcquiz/questions/splk-1003.yaml")
    qz = Quiz(app.pick(20), view)
    qz.run()