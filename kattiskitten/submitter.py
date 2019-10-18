import requests
import configparser
import os
from pathlib import Path
import re
import webbrowser
import sys

_HEADERS = {'User-Agent': 'kattis-cli-submit'}

def get_url(cfg, option, default):
    if cfg.has_option('kattis', option):
        return cfg.get('kattis', option)
    else:
        return 'https://%s/%s' % (cfg.get('kattis', 'hostname'), default)

def get_config():
    cfg = configparser.ConfigParser()

    if not cfg.read([os.path.join(Path.home(), '.kattisrc'),
                     os.path.join(os.path.dirname(sys.argv[0]), '.kattisrc')]):
        raise EnvironmentError(
            "Couldn't find .kattisrc. Please download from https://open.kattis.com/download/kattisrc")
    return cfg
def login(login_url, username, password=None, token=None):
    login_args = {'user': username, 'script': 'true'}
    if password:
        login_args['password'] = password
    if token:
        login_args['token'] = token

    return requests.post(login_url, data=login_args, headers=_HEADERS)

def login_from_config(cfg):
    username = cfg.get('user', 'username')
    password = token = None
    try:
        password = cfg.get('user', 'password')
    except configparser.NoOptionError:
        pass
    try:
        token = cfg.get('user', 'token')
    except configparser.NoOptionError:
        pass
    if password is None and token is None:
        raise EnvironmentError('Invalid .kattisrc file')

    loginurl = get_url(cfg, 'loginurl', 'login')
    return login(loginurl, username, password, token)

def open_submission(submit_response, cfg):
    submissions_url = get_url(cfg, 'submissionsurl', 'submissions')

    m = re.search(r'Submission ID: (\d+)', submit_response)
    if m:
        submission_id = m.group(1)
        url = '%s/%s' % (submissions_url, submission_id)
        webbrowser.open(url)
            

def submit_problem(problem, sub_files, open=True):
    cfg = get_config()
    login_reply = login_from_config(cfg)

    data = {'submit': 'true',
            'submit_ctr': 2,
            'language': 'Python 3',
            'mainclass': 'solution.py',
            'problem': problem,
            'tag': '',
            'script': 'true'}

    result = requests.post(get_url(cfg, 'submissionurl', 'submit'), data=data, files=sub_files, cookies=login_reply.cookies, headers=_HEADERS)

    plain_result = result.content.decode('utf-8').replace('<br />', '\n')
    print(plain_result)
    
    if open: open_submission(plain_result, cfg)