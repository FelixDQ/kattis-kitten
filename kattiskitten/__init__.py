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
import sys
import webbrowser
from kattiskitten.tester import test_problem
from kattiskitten.scraper import get_problem_score
from kattiskitten.submitter import submit_problem

__author__ = "Felix Qvist"

@click.group()
def main():
    """
    Simple CLI for downloading and testing kattis problems
    """
    pass

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

    sub_files = []
    with open(f) as sub_file:
        sub_files.append(('sub_file[]', (os.path.basename(
            f), sub_file.read(), 'application/octet-stream')))

    submit_problem(problem, sub_files)

if __name__ == "__main__":
    main()
