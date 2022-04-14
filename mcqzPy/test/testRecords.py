#!/usr/bin/python3

import os, unittest

from app.Records import Interface
from app.Components import Question

class InterfaceTablesTestCase(unittest.TestCase):

    def setUp(self):
        test_db = "/tmp/testRecords.sqlite.db"
        if os.path.exists(test_db):
            os.remove(test_db)
        self.records = Interface(test_db)

    def testTableCreation(self):
        self.records.c.execute("SELECT name FROM sqlite_schema WHERE type='table'")
        results = [_r[0] for _r in self.records.c.fetchall()]
        for tname in ["question", "quiz", "questionSet", "questionHistory"]:
            with self.subTest(tname):
                self.assertTrue(tname in results)


class InterfaceInsertsTestCase(unittest.TestCase):

    def setUp(self):
        test_db = "/tmp/testRecords.sqlite.db"
        if os.path.exists(test_db):
            os.remove(test_db)
        self.records = Interface(test_db)

    def testInsertQuestionSetInserts(self):
        result = self.records.insert_question_set("Test Set Name")
        self.assertEqual(result, 1)

    def testInsertQuestion(self):
        result = self.records.insert_question(0, "F"*32)
        self.assertEqual(result, 1)

    def testInsertQuiz(self):
        result = self.records.insert_quiz(0, "2022-01-01 00:00:00", 1000)
        self.assertEqual(result, 1)

    def testInsertQuestionHistory(self):
        result = self.records.insert_question_history(0, 0, 1)
        self.assertEqual(result, 1)


class InterfaceRecordResultsTestCase(unittest.TestCase):

    def setUp(self):
        test_db = "/tmp/testRecords.sqlite.db"
        if os.path.exists(test_db):
            os.remove(test_db)
        self.records = Interface(test_db)

    def testRecordQuizInserts(self):
        _q = Question(0, "test", "", [], [])
        result = self.records.record_quiz_results(0, "2022-01-01 00:00:00", 1000, [_q], [1])
        self.assertEqual(result, 1)


class InterfaceExistsTestCase(unittest.TestCase):

    def setUp(self):
        test_db = "/tmp/testRecords.sqlite.db"
        if os.path.exists(test_db):
            os.remove(test_db)
        self.records = Interface(test_db)
        self.records.insert_question_set("Test1")
        self.records.insert_question_set("Test2")
        self.records.insert_question(0, "F"*32)
        self.records.insert_question(0, "E"*32)
        
    def testQuestionSetExistsTrue1(self):
        result = self.records.question_set_exists("Test1")
        self.assertEqual(1, result)

    def testQuestionSetExistsTrue2(self):
        result = self.records.question_set_exists("Test2")
        self.assertEqual(2, result)
    
    def testQuestionSetExistsFalse(self):
        result = self.records.question_set_exists("Test3")
        self.assertFalse(result)
    
    def testQuestionExistsTrueF(self):
        result = self.records.question_exists("F"*32)
        self.assertEqual(1, result)

    def testQuestionExistsTrueE(self):
        result = self.records.question_exists("E"*32)
        self.assertEqual(2, result)

    def testQuestionExistsFalse(self):
        result = self.records.question_exists("0"*32)
        self.assertFalse(result)






if __name__ == "__main__":
    unittest.main()
