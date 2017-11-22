# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from resources.models import *
from rating.models import *
from django.utils import timezone

# Create your tests here.

class Resource_TestCase(TestCase):
    def setUp(self):
        self.r = Resource.objects.create(section="test",content='{"kind": "lesson", "title": "Fonctions de référence", "author": "Paul Robaux"}  ')
        self.u = User.objects.create(first_name="Bib",last_name="my",username='user1')
        self.u1 = User.objects.create(first_name="DBib",last_name="myD",username='user2')
        self.u2 = User.objects.create(first_name="DBiDb",last_name="myFD",username='user3')
        self.d = timezone.now()
        self.prof = Professor.objects.create(user=self.u,nbr_4_star_res=0,status= {'status':'ye'},id=1)
        self.prof2 = Professor.objects.create(user=self.u1,nbr_4_star_res=0,status= {'status':'ye'},id=2)
        self.stud = Student.objects.create(user=self.u2)
        self.q1 = Question.objects.create(question_statement="Did you like it?",type=1)
        self.a1 = Answer.objects.create(answer_statement="Yes, id did")

    def test_resource_add_star_rating(self):
        t = self.r.add_star(2,self.u)
        star_rating = Star_rating.objects.get(id=t.id)
        self.assertEqual(star_rating.star,2)
        self.assertEqual(Star_rating.objects.count(),1)
        self.assertEqual(star_rating.rated_by,self.u)
        """Update star"""
        t = self.r.add_star(3,self.u)
        star_rating = Star_rating.objects.get(id=t.id)
        self.assertEqual(star_rating.star, 3)
        self.assertEqual(Star_rating.objects.count(), 1)
        """Add new star"""
        t = self.r.add_star(2.4,self.u1)
        star_rating = Star_rating.objects.get(id=t.id)
        self.assertEqual(star_rating.star, 2.4)
        self.assertEqual(Star_rating.objects.count(), 2)

    def test_average_resource(self):
        self.r.add_star(5, self.prof.user)
        self.r.add_star(1, self.prof2.user)
        self.r.add_star(3,self.stud.user)
        self.assertEqual(self.r.average(),(3.0,3.0))

class Resource_Rating_TestCase(TestCase):
    def setUp(self):
        self.u = User.objects.create(
            first_name="Bib",
            last_name="my",
            username='user1'
        )
        self.u1 = User.objects.create(
            first_name="DBib",
            last_name="myD",
            username='user2'
        )
        self.u2 = User.objects.create(
            first_name="DBiDb",
            last_name="myFD",
            username='user3'
        )
        self.d = timezone.now()
        self.prof = Professor.objects.create(
            user=self.u,
            nbr_4_star_res=0,
            status={'status': 'ye'}
        )
        self.prof2 = Professor.objects.create(
            user=self.u1,
            nbr_4_star_res=0,
            status={'status': 'ye'}
        )
        self.stud = Student.objects.create(user=self.u2)
        self.q1 = Question.objects.create(question_statement="Did you like it?", type=1)
        self.a1 = Answer.objects.create(answer_statement="Yes, id did")
        self.a2 = Answer.objects.create(answer_statement="Amazing")
        self.r = Resource.objects.create(
            section="test",
            content='{"kind": "lesson", "title": "Fonctions de référence", "author": "Paul Robaux"}',
            added_by = self.u
        )

    def test_add_question_rating(self):
        """"""
        """Rate own resource"""
        qr = self.r.add_rating(question=self.q1,answer=self.a1,user=self.prof.user)
        self.assertEqual(qr,None)
        self.assertEqual(Rating.objects.count(),0)
        """Rate someone elses resource"""
        qr = self.r.add_rating(question=self.q1,answer=self.a1,user=self.prof2.user)
        self.assertEqual(Rating.objects.count(), 1)

    def test_update_rating(self):
        """"""
        """Add Rating and modify it"""
        qr = self.r.add_rating(question=self.q1, answer=self.a1, user=self.prof2.user)
        qr = self.r.add_rating(question=self.q1, answer=self.a2, user=self.prof2.user)
        self.assertEqual(Rating.objects.count(), 1)
        self.assertEqual(Rating.objects.get(pk=qr.id).answer,self.a2)

class Get_Votes_Quetion(TestCase):
    def setUp(self):
        self.q1 = Question.objects.create(question_statement="abba baba", type=0)
        self.q2 = Question.objects.create(question_statement="Enjoyed", type=0)
        self.a1 = Answer.objects.create(answer_statement="Yeah")
        self.a2 = Answer.objects.create(answer_statement="Bee")
        self.u = User.objects.create(first_name="Bib", last_name="zmy", username='user1')
        self.u1 = User.objects.create(first_name="Bideb", last_name="mdy", username='user2')
        self.u2 = User.objects.create(first_name="Bzzfib", last_name="mzy", username='user3')
        self.u3 = User.objects.create(first_name="Bfezzfib", last_name="mzvey", username='user4')
        self.r1 = Resource.objects.create(section="test", content='{"kind": "lesson", "title": "Fonctions de référence", "author": "Paul Robaux"}  ')
        self.d1 = timezone.now()
        self.qq1 = Questionnaire.objects.create(question=self.q1, answer=self.a1)
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