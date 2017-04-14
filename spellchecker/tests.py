from django.test import TestCase

from spellchecker.views import spell_check_api
# Create your tests here.
class SpellCheckerTest(TestCase):
    
    def test_retrieves_correct_html(self):
        response = self.client.get('/spell-checker/')
        self.assertTemplateUsed(response, 'spell_checker.html')

    def test_spell_check_api_retrieves_data(self):
        text_to_check = 'expampl text to chec'
        response = spell_check_api(text_to_check)
        self.assertEquals(response.status_code, 200)

    def test_can_retrieves_expected_text_after_POST(self):
        text_to_check = 'exampl text to chek'
        language = 'English'
        response = self.client.post(
            '/spell-checker/spell-check',
            data = {
                'text-to-check': text_to_check,
            }
        )

        self.assertTemplateUsed(response, 'spell_checker.html')        
        expected_text = 'example text to check'
        self.assertContains(response, expected_text)    
