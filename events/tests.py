"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from events.models import Ticket,Event,Promotion
import datetime


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class CallbackTest(TestCase):
  def setUp(self):
    self.client = Client()
    self.p = Promotion()
    self.e = Event(promotion=self.p,date=datetime.date.today())
    self.t = Ticket(id=1,event=self.e)
    print self.t
  def test_callback_post(self):
    response = self.client.post('/callback/',{'authcode':'TEST',
                                              'billingemail':'test@callback.com',
                                              'billingfirstname':'testy',
                                              'billinglastname':'testington',
                                              'billingpostcode':'SW11RZ',
                                              'billingprefixname':'Mr',
                                              'billingtelephone':'0987654321',
                                              'errorcode':'0',
                                              'mainamount':'50.00',
                                              'orderreference':'1',
                                              'securityresponsesecuritycode':'not yet',
                                              'status':'100',
                                              'transactionreference':'7-9-123456',
                                              })
    print response.content
