from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver

import sys
import time

class FunctionalTest(StaticLiveServerTestCase):
    
    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://'+ arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_enter_a_text_to_check(self):
        # Bob knows this spell-checker website. He goes to check out its spell-check page.
        self.browser.get(self.server_url + '/spell-checker/')

        # He notices the page title and header mention Spell-Checker
        self.assertIn('Spell-Checker', self.browser.title)
        header = self.browser.find_element_by_tag_name('h1')
        self.assertIn('Spell-Checker', header.text)

        # He is invited to enter a text to check
        text_area = self.browser.find_element_by_id('text-to-check')
        self.assertEqual(text_area.get_attribute('placeholder'), 'Enter a text to check')

        # He types "this is a tet abot this awsome functionaliti"
        text_area.send_keys('this is a test abot this awsome functionaliti')

        # When he clicks submit, the page updates and shows the expected text "this is a test about this awesome functionality". And the original text is still there
        text_area.submit()
        time.sleep(3)

        expected_text = self.browser.find_element_by_id('expected-text')
        self.assertEqual(expected_text.text, 'this is a test about this awesome functionality')
        text_area = self.browser.find_element_by_id('text-to-check')
        self.assertEqual(text_area.text, 'this is a test abot this awsome functionaliti')

        # He replace the original text with "Ete es un tes sobe esta increibe funcionalida" and again, when he hits Enter, the page updates and shows the expected text "Este es un test sobre esta increible funcionalidad"
        text_area.clear()
        text_area.send_keys('Ete es un tes sobe esta increibe funcionalida')
        text_area.submit()
        time.sleep(3)
        expected_text = self.browser.find_element_by_id('expected-text')
        self.assertEqual(expected_text.text, 'Este es un test sobre esta increible funcionalidad')

        # Satistfied, He leave the page.
        