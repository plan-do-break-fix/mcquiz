#!/usr/bin/python3

from os import system
import re
from typing import List

from Components import LABELS


class View:

    def clear(self) -> None:
        system("clear")

    def display(self, _q) -> None:
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

    def respond_correct(self) -> None:
        print("\nThat is correct! Keep studying.")

    def respond_incorrect(self, _q) -> None:
        print("\nThat is not correct! You are great disappoint.")
        if _q.qtype == "provide":
            print(f"The correct answer is: {_q.correct}")
        elif _q.qtype == "choose":
            print(f"The correct answer is {', '.join(_q.correct)}")

    def display_final(self, n_correct, score) -> None:
        print(f"You got {n_correct} / 20 questions correct. Score: {score}")

    def advance_prompt(self) -> None:
        input("\n\nPress enter for the next question.")

    # TODO
    def display_marks(self, marks: List[int]) -> str:
        marks_display = ""
        for _i in marks:
            marks_display += "+" if _i else "·"
        while len(marks_display) < 20:
            marks_display += "-"
        return marks_display

    def qheader(self, marks: List[int]) -> None:
        qnum = len(marks) + 1
        marks = self.display_marks(marks)
        print(f"\nQuestion {qnum} / 20 |  {marks}\n")
