import requests
import configparser
import os
from pathlib import Path
import re
import webbrowser
import sys
import kattiskitten.language_detector as language_detector
import kattiskitten.config as cfg

_HEADERS = {'User-Agent': 'kattis-cli-submit'}

def get_active_org():
    return cfg.get('active_org') or 'open.kattis.com'

def get_url(path):
    return 'https://%s/%s' % (get_active_org(), path)

def login(login_url, username, token=None):
    login_args = {'user': username, 'script': 'true', 'token': token}
    return requests.post(login_url, data=login_args, headers=_HEADERS)

def login_from_config():
    org = get_active_org()

    username = cfg.get('username', org)
    token = cfg.get('token', org)
    loginurl = get_url('login')

    return login(loginurl, username, token)

def open_submission(submit_response):
    submissions_url = get_url('submissions')

    m = re.search(r'Submission ID: (\d+)', submit_response)
    if m:
        submission_id = m.group(1)
        url = '%s/%s' % (submissions_url, submission_id)
        webbrowser.open(url)
            

def submit_problem(problem, sub_files, open=True):
    lang = language_detector.determine_language(problem)
    lang_config = language_detector.get_config(lang)

    login_reply = login_from_config()
    data = {'submit': 'true',
            'submit_ctr': 2,
            'language': lang_config.kattis_name,
            'mainclass': lang_config.main_class,
            'problem': problem,
            'tag': 'Submitted with kattis kitten 🦄',
            'script': 'true'}

    result = requests.post(get_url('submit'), data=data, files=sub_files, cookies=login_reply.cookies, headers=_HEADERS)

    plain_result = result.content.decode('utf-8').replace('<br />', '\n')
    if len(plain_result) < 1000:
        print(plain_result)
        if open: open_submission(plain_result)
    else:
        print("Authentication failed :/")
        print("Reauthenticate with \"kk org add\"")