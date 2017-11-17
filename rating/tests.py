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
        qaire_t = Questionnaire.objects.get(pk=self.qaire.id)
        self.assertEqual(qaire_t.question.question_statement,self.q1.question_statement)
        self.assertEqual(qaire_t.answer.answer_statement,self.a1.answer_statement)

    def test_questionnaire_question(self):
        qaire_t = Questionnaire.objects.get(question=self.q1)
        self.assertEqual(self.qaire.id, qaire_t.pk)

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

class Get_Question_Votes_TestCase(TestCase):
    def setUp(self):
        self.q1 = Question.objects.create(question_statement="abba baba", type=0)
        self.q2 = Question.objects.create(question_statement="Enjoyed", type=0)
        self.a1 = Answer.objects.create(answer_statement="Yeah")
        self.a2 = Answer.objects.create(answer_statement="Bee")
        self.u = User.objects.create(first_name="Bib",last_name="zmy",username='user1')
        self.u1 = User.objects.create(first_name="Bideb",last_name="mdy",username='user2')
        self.u2 = User.objects.create(first_name="Bzzfib",last_name="mzy",username='user3')
        self.u3 = User.objects.create(first_name="Bfezzfib",last_name="mzvey",username='user4')
        self.r1 = Resource.objects.create(section="test", content='{"kind": "lesson", "title": "Fonctions de référence", "author": "Paul Robaux"}  ')
        self.d1 = timezone.now()
        self.qq1 = Questionnaire.objects.create(question=self.q1,answer=self.a1)
        self.qq2 = Questionnaire.objects.create(question=self.q1, answer=self.a2)
        self.qq2 = Questionnaire.objects.create(question=self.q2, answer=self.a1)
        self.qq2 = Questionnaire.objects.create(question=self.q2, answer=self.a2)
        self.ra1 = Rating.objects.create(resource=self.r1, question=self.q1, answer=self.a1, rated_by=self.u,rated_on=self.d1)
        self.ra2 = Rating.objects.create(resource=self.r1, question=self.q1, answer=self.a1, rated_by=self.u1,rated_on=self.d1)
        self.ra3 = Rating.objects.create(resource=self.r1, question=self.q1, answer=self.a2, rated_by=self.u2,rated_on=self.d1)
        self.ra2 = Rating.objects.create(resource=self.r1, question=self.q2, answer=self.a1, rated_by=self.u3,rated_on=self.d1)


    def test_get_vote(self):
        dict = self.r1.get_votes_question(question=self.q1)
        self.assertEqual(dict[self.a1.id],2)
        self.assertEqual(dict[self.a2.id],1)
        dict = self.r1.get_votes_question(question=self.q2)
        self.assertEqual(dict[self.a1.id], 1)
        self.assertEqual(dict[self.a2.id], 0)