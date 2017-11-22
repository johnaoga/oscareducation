# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from rating.models import Star_rating,Rating,Questionnaire
from django.utils import timezone
from users.models import Professor,Student
from django.db.models import Count


"""resources models"""


#main resource Model
class Resource(models.Model):

    #@todo section is resource added from where (example : excercie, lesson ...)
    section = models.CharField(max_length=255,null=True,blank=True)
    #json fromat describe resource item
    content = JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(User, null=True)


    def add_star(self, rate, user):
        """
        Creates or modifies the star rating for a resource by a user

        :param rate: float number of stars given
        :param user: user who is giving the stars
        :return: the star object or None is the user can not rate the resource because he uploaded it
        """
        if self.added_by == user:
            return None
        star = Star_rating.objects.filter(resource=self,rated_by=user)
        if star.exists() and len(star) == 1:
            star= star.first()
            star.star = rate
            star.save()
        elif not star.exists() and len(star) == 0:
            star = Star_rating.objects.create(resource=self,star=rate,rated_by=user,rated_on=timezone.now())
        else:
            #Error
            return None
        return star

    def average(self):
        """

        :return: A tuple containing the average for students and average for professors
        """
        all = Star_rating.objects.filter(resource=self)
        prof_nb = 0
        student_nb = 0
        star_prof = 0
        star_student = 0
        for e in all:
            try:
                prof = Professor.objects.get(user=e.rated_by)
            except Professor.DoesNotExist:
                prof = None
            try:
                student = Student.objects.get(user=e.rated_by)
            except Student.DoesNotExist:
                student = None
            if prof != None:
                prof_nb = prof_nb + 1
                star_prof = star_prof + e.star
            if student != None:
                student_nb = student_nb + 1
                star_student = star_student + e.star

        if student_nb==0:
            if prof_nb==0:
                return (0,0)
            else:
                return (0, star_prof / prof_nb)
        else:
            if prof_nb==0:
                return (star_student / student_nb,0)
            else:
                return (star_student / student_nb, star_prof / prof_nb)

    def add_rating(self,question,value,user):
        """
        Creates or Modifies a question/answer to a resource by a user

        :param question: the question answered by user with answer
        :param answer: the answer to question by user
        :param user: User rating resource
        :return: Rating object or None if the user may not rate the resource
        """
        if user == self.added_by:
            return None
        rating = Rating.objects.filter(resource=self,rated_by=user,question=question)
        if rating.exists() and len(rating)==1:
            rating = rating.first()
            rating.question = question
            rating.answer = value
            rating.rated_on = timezone.now()
            rating.save()
        elif not rating.exists():
            rating = Rating.objects.create(
                resource=self,
                question=question,
                answer=value,
                rated_by=user,
                rated_on=timezone.now()
            )
        else:
            #Error
            return None
        return rating

    def get_rating(self,user):
        """

        :param user: User who rated the resource
        :return:
        """
        if  self.added_by == user:
            return None
        ratings = Rating.objects.filter(user=user,resource=self)
        if not ratings.exists():
            return None
        return ratings

    def get_votes_question(self,question):
        """

        :param question: the question we want to get all the answer votes from
        :return: a dictionnary with the answer id as key and the number of votes as value for a specific question on a resource
        """
        total_answers = Questionnaire.objects.filter(question=question).values('answer')
        Qset_rating = Rating.objects.filter(resource=self,question=question)
        #ratings = answers.values('answer').annotate(num_answer=Count('answer')).order_by()
        result = {}
        for answer in total_answers:
            a_id= int(answer['answer'])
            result[a_id] = Qset_rating.filter(answer=a_id).count()
        return result


#khanAcademy video reference data parsed from source url

class KhanAcademy(models.Model):
    #subject
    subject = models.CharField(max_length=255)
    topic = models.CharField(max_length=255, blank=True, null=True)
    tutorial = models.CharField(max_length=255)
    #youtube id
    youtube_id = models.CharField(max_length=25, unique=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100)
    duration = models.PositiveSmallIntegerField()
    fr_date_added = models.DateField(null=True, blank=True)
    class Meta:
        ordering = ['subject', 'topic', 'title']



#ressource refrence from Sesamath
class Sesamath(models.Model):
    classe_int = models.PositiveSmallIntegerField()
    classe = models.CharField(max_length=255)
    # cahier, manuel
    ressource_kind = models.CharField(max_length=255)
    chapitre = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    # "Fiche/Page"
    section_kind = models.CharField(max_length=255)
    year = models.PositiveSmallIntegerField(blank=True, null=True)
    file_name = models.CharField(max_length=255)
    on_oscar = models.URLField(unique=True)

    def ressource_kind_with_year(self):
        if self.year:
            return u"%s - %s" % (self.year, self.ressource_kind)
        return self.ressource_kind

    class Meta:
        ordering = [
            'classe_int',
            'year',
            'ressource_kind',
            'chapitre',
            'section_kind',
        ]