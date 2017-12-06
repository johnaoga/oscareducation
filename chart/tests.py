#!/usr/bin/env python3
# coding: utf-8

# Add your tests in this file
# pyhamcrest has to be installed
# doc: http://pyhamcrest.readthedocs.io/en/release-1.8/tutorial/

import unittest
# from selenium import webdriver
# from selenium.webdriver.comm.keys import Keys
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.support import WebDriverWait
from chart.evaluate_chart import evaluate_chart
from examinations.models import Question
from django.test import TestCase
import types

# class TeacherSide(unittest.TestCase):
#
# 	def setUp(self):
# 		self.driver = webdriver.Firefox()
# 		driver = self.driver
# 		driver.get("http://127.0.01:8000")
# 		wait = WebDriverWait(driver, 10)
# 		#assert "No results found." not in driver.page_source
#
# 	def tearDown(self):
# 		self.driver.close()


class CorrectionChartExercices(TestCase):
    def setUp(self):
        commonQparts = ["type: ","""\nanswers:""","""\n- chart: '{"point":""",
						""","AxisX":"abscisses","AxisY":"ordonnees","zeroX":-1,"zeroY":-1,"maxX":10,"maxY":10}'"""]
        setOfTest = [['chart-barchart', '[1,1,1,2]', [u'1,1,2'], 0,'response of different lenght shouldnt be considere as a True answer'],
					 ['chart-barchart', '[1,1,1,2]', [u'1,1,1,2'], 1,'same answer should be True'],
                     ['chart-barchart','[2,2,2,2,2]',[u'1,1,2,2,2'],0,'answer different but of same length'],
                     ['chart-barchart','',[u'1,2,1'],-1,'without true answer, it is impossible to correct'],
                     ['chart-barchart',['[1,2,1,1]','[1,2,2,1]','[1,2,2,2]'],[u'1,1,1,1'],0,'answer different but of same length, multiple possible answer'],
                     ['chart-barchart', ['[1,2,1,1]', '[1,2,2]', '[1,2,2,2,2]'], [u'1,1,1,1'], 0,'answer different but of same length, multiple possible answer with different length'],
                     ['chart-barchart', ['[1,2,1,1]', '[1,2,2]', '[1,2,2,2,2]'], [u'1,2,2'], 1,'answer correct but of same length, multiple possible answer'],
                     ['chart-barchart', ['[1,2,1,1]', '[1,2,2]', '[1,2,2,2]'], [u'1,1,1,1,1'], 0,'answer different but of different length, multiple possible answer'],
                     ['chart-barchart', ['[1,2,1,1]', '[1,2,2]', '[1,2,2,2]'], [u'1,2,2,2'], 1,'answer correct but of same length, multiple possible answer, last is the one'],
                     ['chart-barchart', '[]', [u''], 1,'empty answer with empty correct answer - fundamentaly correct'],
                     ['chart-barchart', '[1,1]', [u''], 0,'empty answer with non empty correct answer - fundamentaly incorrect'],
                     ['chart-piechart','"[secteur:90,secteur:90,secteur:180]"',[u'secteur:90,secteur:90,secteur:180'],1,'simple correct answer'],
                     ['chart-piechart', '"[secteur:90,secteur:90,secteur:180]"', [u'secteur:50,secteur:90,secteur:180'],0, 'the first sector is different'],
                     ['chart-piechart', '"[secteur:90,secteur:90,secteur:180]"', [u'secteur:90,secteur:90,secteur:190'],0, 'the last sector is different and over 360 degrees'],
                     ['chart-piechart', '"[secteur:90,secteur:90,secteur:180]"', [u''],0, 'no answer'],
                     ['chart-piechart', '"[secteur:50,secteur:180,secteur:90,secteur:40]"', [u'secteur:90,secteur:50,secteur:40,secteur:180'],1, 'correct answer with shuffle the sectors'],
                     ['chart-piechart', '"[secteur:50,s1:180,s2:90,s3:40]"',[u's2:90,secteur:50,s3:40,s1:180'], 1, 'correct answer with shuffle the sectors and different sectors name'],
                     ['chart-piechart', '"[secteur:90,secteur:90,secteur:180]"', [u'secteur:90,s:90,secteur:180'],0, 'only names does not match'],
                     ['chart-piechart', ['"[secteur:90,secteur:90,secteur:180]"','"[secteur:50,s:130,secteur:180]"'], [u'secteur:50,s:130,secteur:180'], 1,'multiple answer are possible - the propose answer match'],
                     ['chart-piechart', ['"[secteur:90,secteur:90,secteur:180]"', '"[secteur:50,s:130,secteur:180]"'],[u'secteur:50,se:130,secteur:180'], 0, 'multiple answer are possible - the propose answer does not match'],
                     ['chart-piechart', ['"[secteur:90,secteur:90,secteur:180]"', '"[secteur:50,s:130,secteur:180,sec:80]"'], [u'secteur:50,s:130,sec:80,secteur:180'], 1, 'multiple answer are possible - the propose answer match']]
        self.studentAnswer = []
        self.output = []
        self.message = []
        for (test,i) in zip(setOfTest,range(len(setOfTest))):
            if isinstance(test[1],types.StringTypes):
                ans = commonQparts[0]+test[0]+commonQparts[1]+commonQparts[2]+test[1]+commonQparts[3]
            else:
                ans = commonQparts[0]+test[0]+commonQparts[1]
                for x in test[1]:
                    ans += commonQparts[2]+x+commonQparts[3]
            Question.objects.create(description=('Q'+str(i)),answer=ans,source="None",indication=test[0])

            self.studentAnswer.append(test[2])
            self.output.append(test[3])
            self.message.append(test[4])

    def testBarchart(self):
        for i in range(len(self.studentAnswer)):
            Q = Question.objects.get(description='Q'+str(i))
            if Q.indication == "chart-barchart":
                self.assertEqual(evaluate_chart(Q,self.studentAnswer[i]),self.output[i],self.message[i])


    def testPiechart(self):
        for i in range(len(self.studentAnswer)):
            Q = Question.objects.get(description='Q'+str(i))
            if Q.indication == "chart-piechart":
                self.assertEqual(evaluate_chart(Q,self.studentAnswer[i]),self.output[i],self.message[i])

if __name__ == '__main__':
	unittest.main()

