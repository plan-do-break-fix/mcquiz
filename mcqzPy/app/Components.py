#!/usr/bin/python3

from dataclasses import dataclass
from random import shuffle
from typing import List

LABELS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

@dataclass
class ViewParams:
    #qtypes: list
    prompts: str = "None"
    assist: str = "None"

@dataclass
class QuestionParams:
    qtype: str
    shuffle: bool
    strict_order: bool

@dataclass
class QuizParams:
    n_questions: int
    max_score: int
    time_limit: bool = None

@dataclass
class Question:
    qtype: str
    question: str
    correct: list[str]
    choices: list[str]
    params: QuestionParams = None

    def check(self, answer: list[str]) -> bool:
        return answer == self.correct


class Quiz:

    def __init__(self, questions: List[Question], view, params=None) -> None:
        self.questions = questions
        self.marks = []
        self.view = view
    
    def run(self):
        for _q in self.questions:
            self.view.clear()
            self.view.qheader(self.marks)
            self.view.display(_q)
            user_answer = self.view.prompt(_q)
            if _q.check(user_answer):
                self.marks.append(1)
                self.view.respond_correct()
            else:
                self.marks.append(0)
                self.view.respond_incorrect(_q)
            self.view.advance_prompt()
        n_correct = sum(self.marks)
        score = n_correct * 50
        self.view.display_final(n_correct, score)