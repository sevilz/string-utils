from django.shortcuts import render
from django.http import HttpRequest
from django.conf import settings
from django.views.decorators.http import require_POST

import requests


API_KEY = getattr(settings, 'BING_SPELL_CHECK_API_KEY')
API_ENDPOINT = getattr(settings, 'BING_SPELL_CHECK_ENDPOINT')

def view_spellchecker(request):
    return render(request, 'spell_checker.html')

@require_POST
def spellcheck(request):
    text_to_check = request.POST['text-to-check']
    language = request.POST['text-to-check']
    text_checked = spell_check_text(text_to_check)
    fields = {
        'text_to_check': request.POST['text-to-check'],
    }
    return render(request, 'spell_checker.html', {'text_checked': text_checked, 'fields': fields})

def spell_check_text(text_to_check):
    text_checked = text_to_check
    response = spell_check_api(text_to_check)
    flaggedTokens = response.json()['flaggedTokens']
    for flaggedToken in flaggedTokens:
        original_word = flaggedToken['token']
        first_suggested_word = flaggedToken['suggestions'][0]['suggestion']
        text_checked = text_checked.replace(original_word, first_suggested_word)
    return text_checked

def spell_check_api(text, mode='proof'):
    url = '{endpoint}?text={text}&mode={mode}'.format(endpoint=API_ENDPOINT, text=text, mode=mode)
    headers = {'Ocp-Apim-Subscription-Key': API_KEY}
    response = requests.get(url, headers=headers)
    return response
