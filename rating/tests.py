# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rating.models import *
from django.test import TestCase
from resources.models import *
from django.utils import timezone

# Tests for the classe Star_rating
class Star_rating_TestCase(TestCase):
    def setUp(self):
        d = timezone.now()
        u = User.objects.create()
        r = Resource.objects.create(section="test",content='{"kind": "lesson", "title": "Fonctions de référence", "author": "Paul Robaux"}  ')
        o = Star_rating.objects.create(
            star=2,
            resource=r,
            rated_by=u,
            rated_on=d,
        )
        self.date = d
        self.id= o.id

    def test_star_in_table(self):
        star_r = Star_rating.objects.get(id=self.id)
        self.assertEqual(star_r.star,2)

# Tests for the class Answer
class Answer_TestCase(TestCase):
    def setUp(self):
        self.ob1 = Answer.objects.create(answer_statement = "Nous sommes le 31 octobre")
        self.ob2 = Answer.objects.create(answer_statement = " Yes we can")


    def test_answer_in_table(self):
        ans1 = Answer.objects.get(pk=self.ob1.id)
        self.assertEqual(ans1.answer_statement, "Nous sommes le 31 octobre")    # True
        ans2 = Answer.objects.get(pk=self.ob2.id)
        self.assertEqual(ans2.answer_statement, " Yes we can")                  # False


# Tests for the class Questin
class Question_TestCase(TestCase):
    def setUp(self):
        self.ob3 = Question.objects.create(question_statement = "Quel date sommes-nous?", type = 0)
        self.ob4 = Question.objects.create(question_statement = "Can we do this ?", type = 1)

    def test_question_in_table(self):
        ques1 = Question.objects.get(pk=self.ob3.id)
        self.assertEqual(ques1.question_statement, "Quel date sommes-nous?")  # True
        self.assertEqual(ques1.type, 0)                                       # True
        ques2 = Question.objects.get(pk=self.ob4.id)
        self.assertEqual(ques2.question_statement, "Can we do this ?")    # False
        self.assertEqual(ques2.type, 1)
        # False

class Quetionnaire_TestCase(TestCase):
    def setUp(self):
        self.q1 = Question.objects.create(question_statement = "abba baba", type = 0)
        self.a1 = Answer.objects.create(answer_statement = "Yeah")
        self.qaire = Questionnaire.objects.create(question=self.q1,answer=self.a1)

    def test_questionnaire_id(self):
        qaire_t = Questionnaire.objects.get(pk=1)
        self.assertEqual(qaire_t.question.question_statement,self.q1.question_statement)
        self.assertEqual(qaire_t.answer.answer_statement,self.a1.answer_statement)

    def test_questionnaire_question(self):
        qaire_t = Questionnaire.objects.get(question=self.q1)
        self.assertEqual(2, qaire_t.pk)
        '''id=2 because test is called before each test function'''

class Rating_TestCase(TestCase):
    def setUp(self):
        self.q1 = Question.objects.create(question_statement = "abba baba", type = 0)
        self.a1 = Answer.objects.create(answer_statement = "Yeah")
        self.u = User.objects.create()
        self.r1 = Resource.objects.create(section="test",content='{"kind": "lesson", "title": "Fonctions de référence", "author": "Paul Robaux"}  ')
        self.d1 = timezone.now()
        self.ra1 = Rating.objects.create(resource=self.r1,question=self.q1,answer=self.a1,rated_by=self.u,rated_on=self.d1)

    def test_rating(self):
        q = Rating.objects.get(pk=self.ra1.id)
        self.assertEqual(q.answer.answer_statement,self.a1.answer_statement)