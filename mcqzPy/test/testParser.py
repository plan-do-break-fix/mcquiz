#!/usr/bin/python3

import unittest

from app.Parser import Parser

class ParserNormalization(unittest.TestCase):

    def setUp(self):
        self.parser = Parser()

    def testNormalizeCommonChooseQDict(self):
        qdict = {"Question":"", "Correct": "ans1", "Incorrect": ["ans2", "ans3"]}
        expected = {"Question":"", "Correct": ["ans1"], "Incorrect": ["ans2", "ans3"]}
        self.assertDictEqual(expected, self.parser.normalize_qdict(qdict))

    def testNormalizeStringsOnlyQDict(self):
        qdict = {"Question":"", "Correct": "ans1", "Incorrect": "ans2"}
        expected = {"Question":"", "Correct": ["ans1"], "Incorrect": ["ans2"]}
        self.assertDictEqual(expected, self.parser.normalize_qdict(qdict))

    def testNormalizeProvideQDictWithEmptyIncorrect(self):
        qdict = {"Question":"", "Correct": "ans1", "Incorrect": None}
        expected = {"Question":"", "Correct": ["ans1"], "Incorrect": []}
        self.assertDictEqual(expected, self.parser.normalize_qdict(qdict))

    def testNormalizeProvideQDictWithNoIncorrect(self):
        qdict = {"Question":"", "Correct": "ans1"}
        expected = {"Question":"", "Correct": ["ans1"], "Incorrect": []}
        self.assertDictEqual(expected, self.parser.normalize_qdict(qdict))

    def testNormalizeAlreadyNormalProvideQDict(self):
        qdict = {"Question":"", "Correct": ["ans1"], "Incorrect": []}
        self.assertDictEqual(qdict, self.parser.normalize_qdict(qdict))

    def testNormalizeAlreadyNormalChooseQDict(self):
        qdict = {"Question":"", "Correct": ["ans1"], "Incorrect": ["ans2", "ans3"]}
        self.assertDictEqual(qdict, self.parser.normalize_qdict(qdict))

    def testNormalizeAlreadyNormalChooseMultiQDict(self):
        qdict = {"Question":"", "Correct": ["ans1", "ans2"], "Incorrect": ["ans3", "ans4"]}
        self.assertDictEqual(qdict, self.parser.normalize_qdict(qdict))
