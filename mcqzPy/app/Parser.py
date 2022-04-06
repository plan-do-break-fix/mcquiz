#!/usr/bin/python3

from hashlib import md5
from random import shuffle
from typing import List, Tuple
import yaml

from Components import Question, LABELS


class Parser:

    @staticmethod
    def read_qfile(fpath: str) -> List[dict]:
        """
        Returns list of all dictionaries in specified YAML having minimal required keys.
        """
        with open(fpath) as _f:
            raw_read = yaml.safe_load(_f)
        if not type(raw_read) == list:
            raise RuntimeError("Bad YAML input.")
        return [_i for _i in raw_read if type(_i) == dict and "Question" in _i.keys() and "Correct" in _i.keys()]

    @staticmethod
    def prepare_choose_answers(qdict: dict) -> Tuple[List[str], List[str]]:
        """
        Return shuffled answers and answer key for 'choose' type question.
        """
        if type(qdict["Correct"]) == str:
            correct_choices = [(1, qdict["Correct"])]
        elif type(qdict["Correct"]) == list:
            correct_choices = [(1, _i) for _i in qdict["Correct"]]
        incorrect_choices = [(0, _i) for _i in qdict["Incorrect"]]
        choices = correct_choices + incorrect_choices
        if "shuffle" not in qdict.keys() or qdict["shuffle"] == "True":
            shuffle(choices)
        correct = []
        for _i, choice in enumerate(choices):
            if choice[0] == 1:
                correct.append(LABELS[_i])
            choices[_i] = choice[1]
        return (correct, choices)

    @staticmethod
    def normalize_qdict(qdict: dict) -> dict:
        """
        Return qdict with string values for Correct and/or Incorrect transformed into single value lists.
        """
        if ("Incorrect" not in qdict.keys()) or (qdict["Incorrect"] == None):
            qdict["Incorrect"] = []
        for _k in ["Correct", "Incorrect"]:
            if type(qdict[_k]) == str:
                qdict[_k] = [qdict[_k]]
        return qdict

    @staticmethod
    def question_type(normal_qdict: dict) -> str:
        """
        Returns the type of question contained in qdict: boolean, choose, provide
        """
        if len(normal_qdict["Correct"]) == 1:
            if not normal_qdict["Incorrect"]:
                if normal_qdict["Correct"][0] in ["True", "False"]:
                    return "boolean"
                return "provide"
            elif len(normal_qdict["Incorrect"]) == 1:
                _choices = normal_qdict["Incorrect"] + normal_qdict["Correct"]
                _choices.sort()
                if _choices == ["False", "True"]:
                    return "boolean"
        return "choose"

    def prepare_question(self, normal_qdict: dict, qtype: str) -> Question:
        """
        Returns a Quiz Question created with values from the qdict.
        """
        qid: str = normal_qdict["qid"]
        if qtype == "boolean":
            correct, choices = normal_qdict["Correct"], ["True", "False"]
        elif qtype == "provide":
            correct, choices = normal_qdict["Correct"], []
        elif qtype == "choose":
            correct, choices = self.prepare_choose_answers(normal_qdict)
        return Question(qid, qtype, normal_qdict["Question"], correct, choices)

    @staticmethod
    def fingerprint(normal_qdict: dict) -> str:
        return md5(normal_qdict.__repr__().encode()).hexdigest()