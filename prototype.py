#!/usr/bin/python3

from dataclasses import dataclass
import yaml
from random import shuffle
import re
from typing import List, Tuple


LABELS = ["A", "B", "C", "D", "E", "F"]


@dataclass
class QuizQuestion:
    qtype: str
    question: str
    correct: list[str]
    choices: list[str]

    def check(self, answer: list[str]) -> bool:
        return answer == self.correct


class Sprint:

    def __init__(self, fpath: str) -> None:
        self.questions = []
        self.marks = []
        self.view = CliQuizView()
        bank = [Parser.prepare_question(_q) for _q in Parser.read_qfile(fpath)]
        shuffle(bank)
        self.questions = bank[:20]

    def run(self):
        for _i, _q in enumerate(self.questions):
            print(f"\n\n{_i + 1} / 20 -------------------\n")
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


class CliQuizView:

    def display(self, _q):
        print(f"{_q.question}\n\n===\n")
        if _q.choices:
            for _i, choice in enumerate(_q.choices):
                print(f"{LABELS[_i]}.  {choice}")

    def prompt(self, _q) -> List[str]:
        user_answer = input("> ")
        if not user_answer:
            return self.prompt(_q)
        else:
            return self.normalize_answer(user_answer, _q.qtype)

    def normalize_answer(self, answer: str, qtype: str) -> List[str]:
        if qtype == "provide":
            return [answer]
        elif qtype == "choose":
            answer = re.sub(r"(?:\s|,)", "", answer)
            answer = [_char.upper() for _char in answer]
            answer.sort()
            return answer

    def respond_correct(self):
        print("That is correct! Keep studying.")

    def respond_incorrect(self, _q):
        print("That is not correct! You are great disappoint.")
        if _q.qtype == "provide":
            print(f"The correct answer is: {_q['Correct']}")
        elif _q.qtype == "choose":
            print(f"The correct answer is {', '.join(_q.correct)}")

    def display_final(self, n_correct, score) -> None:
        print(f"You got {n_correct} / 20 questions correct. Score: {score}")

    def advance_prompt(self) -> None:
        input("Press enter for the next question.")

class Parser:

    @staticmethod
    def read_qfile(fpath: str) -> List[dict]:
        with open(fpath) as _f:
            raw_read = yaml.safe_load(_f)
        if not type(raw_read) == list:
            raise RuntimeError("Bad YAML input.")
        return [_i for _i in raw_read if type(_i) == dict and "Question" in _i.keys() and "Correct" in _i.keys()]

    @staticmethod
    def prepare_choose_answers(qdict: dict) -> Tuple[List[str], List[str]]:
        if type(qdict["Correct"]) == str:
            correct_choices = [(1, qdict["Correct"])]
        elif type(qdict["Correct"]) == list:
            correct_choices = [(1, _i) for _i in qdict["Correct"]]
        incorrect_choices = [(0, _i) for _i in qdict["Incorrect"]]
        choices = correct_choices + incorrect_choices
        shuffle(choices)
        correct = []
        for _i, choice in enumerate(choices):
            if choice[0] == 1:
                correct.append(LABELS[_i])
            choices[_i] = choice[1]
        return (choices, correct)

    @staticmethod
    def prepare_question(qdict: dict) -> QuizQuestion:
        if "Incorrect" not in qdict.keys() or qdict["Incorrect"] == None:
            qdict["Incorrect"] = []
        if len(qdict["Correct"]) == 1 and not qdict["Incorrect"]:
            qtype: str = "provide"
            choices, correct = [], qdict["Correct"]
        else:
            qtype: str = "choose"
            choices, correct = Parser.prepare_choose_answers(qdict)
        return QuizQuestion(qtype, qdict["Question"], correct, choices)


if __name__ == "__main__":
    sprint = Sprint()
