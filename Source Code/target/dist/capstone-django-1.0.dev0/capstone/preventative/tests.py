import datetime

from django.test import TestCase
from django.utils import timezone
from django.conf import settings

from .models import Document

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Create your tests here.

class DocumentModelTests(TestCase):

    def test_was_published_recently_with_future_document(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_document = Document(uploaded_at=time)
        self.assertIs(future_document.was_published_recently(), False)

    def test_was_published_recently_with_old_document(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_document = Document(uploaded_at=time)
        self.assertIs(old_document.was_published_recently(), False)

    def test_was_published_recently_with_recent_document(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_document = Document(uploaded_at=time)
        self.assertIs(recent_document.was_published_recently(), True)

class AccountTestCase(LiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Firefox(executable_path = settings.BASE_DIR + '\\static\\capstone\\geckodriver.exe')
        super(AccountTestCase, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(AccountTestCase, self).tearDown()

    def test_register(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')
        assert 'Improve Health Care' in selenium.page_source
