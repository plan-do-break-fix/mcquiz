#!/usr/bin/python3

import unittest
import sys

sys.path.append("/home/jswan/mcquiz/mcqzPy/app")
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

class ParserQuestionType(unittest.TestCase):

    def setUp(self):
        self.parser = Parser()

    def testQTypeBooleanCorrectOnlyTrue(self):
        qdict = {"Question":"", "Correct": ["True"], "Incorrect": []}
        self.assertEqual("boolean", self.parser.question_type(qdict))

    def testQTypeBooleanCorrectOnlyFalse(self):
        qdict = {"Question":"", "Correct": ["False"], "Incorrect": []}
        self.assertEqual("boolean", self.parser.question_type(qdict))
        
    def testQTypeBooleanTrueFalse(self):
        qdict = {"Question":"", "Correct": ["True"], "Incorrect": ["False"]}
        self.assertEqual("boolean", self.parser.question_type(qdict))
        
    def testQTypeBooleanFalseTrue(self):
        qdict = {"Question":"", "Correct": ["False"], "Incorrect": ["True"]}
        self.assertEqual("boolean", self.parser.question_type(qdict))
    
    def testQTypeProvide(self):
        qdict = {"Question":"", "Correct": ["Somthing something something"], "Incorrect": []}
        self.assertEqual("provide", self.parser.question_type(qdict))

    def testQTypeChoose(self):
        qdict = {"Question":"", "Correct": ["ans1"], "Incorrect": ["ans2", "ans3"]}
        self.assertEqual("choose", self.parser.question_type(qdict))
        
    def testQTypeChooseMulti(self):
        qdict = {"Question":"", "Correct": ["ans1", "ans2"], "Incorrect": ["ans3", "ans4"]}
        self.assertEqual("choose", self.parser.question_type(qdict))

    def testQTypeChooseMultiAllCorrect(self):
        qdict = {"Question":"", "Correct": ["ans1", "ans2"], "Incorrect": []}
        self.assertEqual("choose", self.parser.question_type(qdict))


class ParserPrepareBooleanQuestion(unittest.TestCase):

    def setUp(self):
        parser = Parser()
        qdict = {"Question":"Shoes before pants.", "Correct": ["True"], "Incorrect": [], "pk": "test"}
        self.q = parser.prepare_question(qdict, "boolean")

    def testPrepareQsBooleanQuestionAttr(self):
        self.assertEqual("Shoes before pants.", self.q.question)

    def testPrepareQsBooleanCorrectAttr(self):
        self.assertEqual(["True"], self.q.correct)

    def testPrepareQsBooleanChoicesAttr(self):
        self.assertEqual(["True", "False"], self.q.choices)


class ParserPrepareProvideQuestion(unittest.TestCase):

    def setUp(self):
        parser = Parser()
        qdict = {"Question":"Shoes _____ pants.", "Correct": ["before"], "Incorrect": [], "pk": "test"}
        self.q = parser.prepare_question(qdict, "provide")

    def testPrepareQsBooleanQuestionAttr(self):
        self.assertEqual("Shoes _____ pants.", self.q.question)

    def testPrepareQsBooleanCorrectAttr(self):
        self.assertEqual(["before"], self.q.correct)

    def testPrepareQsBooleanChoicesAttr(self):
        self.assertEqual([], self.q.choices)

    def testPrepareQspkAttr(self):
        self.assertEqual("test", self.q.pk)


class ParserFingerprint(unittest.TestCase):

    def setUp(self):
        self.parser = Parser()
    
    def testFingerPrintOne(self):
        normal_qdict = {"Question": "", "Correct": ["Two"], "Incorrect": ["Three"]}
        expected = "9cc3161311a6c2d6ba3b3fea4cf46977"
        self.assertEqual(expected, self.parser.fingerprint(normal_qdict))


if __name__ == "__main__":
    unittest.main()
