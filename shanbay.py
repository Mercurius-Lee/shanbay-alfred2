#!/usr/bin/env python
# coding: utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import os
import urllib
import urllib2
import json
import time
import argparse
from urlparse import urlparse
import subprocess

from alfred.feedback import Feedback


TOKEN_FILE = os.path.abspath('token')
CLIENT_ID = '7f652079ade6d4fa4eec'
SEARCH_API_URL = 'https://api.shanbay.com/bdc/search/'
LEARNING_API = 'https://api.shanbay.com/bdc/learning/'
REDIRECT_URI = 'https://api.shanbay.com/oauth2/auth/success/'
ALFRED_WORD_AUDIO_MP3_FILE = '/tmp/alfred_word_audio.mp3'


def _request(path, params=None, method='GET', data=None, headers=None):
    params = params or {}
    headers = headers or {}
    if params:
        url = path + '?' + urllib.urlencode(params)
    else:
        url = path
    
    request = urllib2.Request(url, data, headers)
    request.get_method = lambda: method
    response = urllib2.urlopen(request)
    return response.read()


def _api(path, params=None, method='GET', data=None, headers=None):
    response = _request(path=path, params=params, method=method, data=data,
                        headers=headers)
    result = json.loads(response)
    if result['status_code'] != 0:
        return None
    return result['data']


def save_token(url):
    #url = 'https://api.shanbay.com/oauth2/auth/success/#access_token=JnaN2POht3aaR2IJpfLEV32txhvTqb&token_type=Bearer&state=&expires_in=2592000&scope=read+write'
    parse_result = urlparse(url)
    data = dict(map(lambda x: x.split('='), parse_result.fragment.split('&')))
    data['expires_in'] = int(data['expires_in'])
    data['timestamp'] = time.time()
    with(open(TOKEN_FILE, 'w')) as token_file:
        token_file.write(json.dumps(data))


def search(word):
    feedback = Feedback()
    data = _api(SEARCH_API_URL, params={'word': word})
    if data is None:
        return

    word = data['content']
    pron = data['pron']
    title = "%s [%s]" % (word, pron)
    subtitle = data['definition'].decode("utf-8")
    subtitle = subtitle.replace('\n', ' ') #.replace('&', '')

    feedback.addItem(title=title, subtitle=subtitle, arg=word)
    if data.has_key('en_definitions') and data['en_definitions']:
        for type in data['en_definitions']:
            for line in data['en_definitions'][type]:
                title = type+', '+line
                if not title:
                    continue
                feedback.addItem(title = title, arg = word)
    feedback.output()


def token_url(url):
    if not url.startswith('https://api.shanbay.com/oauth2/auth/success/#'):
        return
    return save_token(url)


def read_token():
    if not os.path.isfile(TOKEN_FILE):
        return False
    token_json = json.loads(open(TOKEN_FILE).read())
    if token_json['timestamp'] + token_json['expires_in'] < int(time.time()):
        return False
    return token_json['access_token']


def learning(word):
    access_token = read_token()
    if not access_token:
        return authorize()
    search_data = _api(SEARCH_API_URL, params={'word': word})
    if search_data is None:
        return
    data = _api(LEARNING_API,
                data=urllib.urlencode({'id': search_data['id']}),
                headers={'Authorization': 'Bearer %s' % access_token},
                method='POST')
    if data is None:
        print('"%s" Add Fail' % word)
        return
    print('"%s" Add Success' % word)


def authorize():
    url = 'https://api.shanbay.com/oauth2/authorize/?client_id=%s&response_type=token' % CLIENT_ID
    os.system('open "%s"' % url)


def sound(word):
    data = _api(SEARCH_API_URL, params={'word': word})
    if data is None:
        return
    audio_address = data['audio_addresses']['us'][0]
    with open(ALFRED_WORD_AUDIO_MP3_FILE, 'w') as f:
        f.write(_request(audio_address))
    subprocess.call(['/usr/bin/afplay', ALFRED_WORD_AUDIO_MP3_FILE])


def open(word):
    data = _api(SEARCH_API_URL, params={'word': word})
    if data is None:
        return
    url = 'http://www.shanbay.com/bdc/vocabulary/%d/' % data['id']
    os.system('open "%s"' % url)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--search', nargs='?', type=str)
    parser.add_argument('--learning', nargs='?')
    parser.add_argument('--tokenurl', nargs='?')
    parser.add_argument('--sound', nargs='?')
    parser.add_argument('--open', nargs='?')
    args = parser.parse_args()

    if args.search:
        search(args.search)
    elif args.learning:
        learning(args.learning)
    elif args.tokenurl:
        token_url(args.tokenurl)
    elif args.sound:
        sound(args.sound)
    elif args.open:
        open(args.open)
    else:
        pass

if __name__ == '__main__':
    main()
