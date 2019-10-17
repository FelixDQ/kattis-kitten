__version__ = "0.1.0"

import click
import requests
import zipfile
import tempfile
import glob
import subprocess
import colorful as cf
import re
import os
import configparser
import sys
import webbrowser
from pathlib import Path
from kattiskitten.tester import test_problem
from kattiskitten.scraper import get_problem_score

__author__ = "Felix Qvist"

_HEADERS = {'User-Agent': 'kattis-cli-submit'}

@click.group()
def main():
    """
    Simple CLI for downloading and testing kattis problems
    """
    pass

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
            
@main.command()
@click.argument('problem')
def test(problem):
    """This tests a kattis problem using provided test problems"""
    if problem == 'all':
        problems = glob.glob(f"./*/")

        completed_count = 0
        total_score = 0
        earned_score = 0
        for p in problems:
            p = re.sub(r'[^\w]', '', p)
            res = test_problem(p, False)
            score = get_problem_score(p)
            total_score += score
            if res:
                print(f"✅ {p}")
                completed_count += 1
                earned_score += score
            else:
                print(f"❌ {p}")

        print(f"\n Completed {completed_count}/{len(problems)}")
        print(f"\n Earned {round(earned_score)}/{round(total_score)} points")

    else:
        res = test_problem(problem)
        if res:
            print(f"Earned {get_problem_score(problem)} points 🎉")


@main.command()
@click.argument('problem')
def get(problem):
    """This command downloads a kattis problem and test files"""
    res = requests.get(
        f"https://open.kattis.com/problems/{problem}/file/statement/samples.zip")

    if res.status_code == 404:
        print(f"Couldn't find problem '{problem}'. Maybe you typed it wrong? Or no test files exist")
    else:
        print("Downloading samples")
        tmp_file = tempfile.NamedTemporaryFile(delete=False)
        open(tmp_file.name, 'wb').write(res.content)

        with zipfile.ZipFile(tmp_file.name, 'r') as zip_ref:
            zip_ref.extractall(f'./{problem}')
            print(f"Samples downloaded to './{problem}'")
        tmp_file.close()
        os.unlink(tmp_file.name)

        # Create main.py with template
        if not os.path.exists(f'./{problem}/main.py'):
            open(f'./{problem}/main.py', 'w').write("""n = int(input())

for i in range(n):
    print(i)
    """)


@main.command()
@click.argument('problem')
def submit(problem):
    """This command submits a problem to kattis"""
    f = f'./{problem}/main.py'
    cfg = get_config()

    login_reply = login_from_config(cfg)



    data = {'submit': 'true',
            'submit_ctr': 2,
            'language': 'Python 3',
            'mainclass': 'main.py',
            'problem': problem,
            'tag': '',
            'script': 'true'}

    sub_files = []
    with open(f) as sub_file:
        sub_files.append(('sub_file[]', (os.path.basename(
            f), sub_file.read(), 'application/octet-stream')))

    result = requests.post(get_url(cfg, 'submissionurl', 'submit'), data=data, files=sub_files, cookies=login_reply.cookies, headers=_HEADERS)

    plain_result = result.content.decode('utf-8').replace('<br />', '\n')
    print(plain_result)
    open_submission(plain_result, cfg)


if __name__ == "__main__":
    main()
