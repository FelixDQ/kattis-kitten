__version__ = "0.1.0"

import configparser
import glob
import os
import re
import subprocess
import sys
import tempfile
import webbrowser
import zipfile

import click
import colorful as cf
import requests

import kattiskitten.config as cfg
import kattiskitten.language_detector
from kattiskitten.submitter import submit_problem
from kattiskitten.tester import test_problem

__author__ = "Felix Qvist"


@click.group()
def main():
    """
    Simple CLI for downloading and testing kattis problems
    """
    print(f"Using {cfg.get('active_org') or 'open.kattis.com'}")
    pass


@main.command()
@click.argument("problem")
def test(problem):
    """This tests a kattis problem using provided test problems"""
    if problem == "all":
        problems = glob.glob(f"./*/")

        completed_count = 0
        total_score = 0
        earned_score = 0
        for p in problems:
            p = re.sub(r"[^\w]", "", p)
            res = test_problem(p, False)
            total_score += score
            if res:
                print(f"✅ {p}")
                completed_count += 1
                earned_score += score
            else:
                print(f"❌ {p}")

        print(f"\n Completed {completed_count}/{len(problems)}")

    else:
        res = test_problem(problem)
        if res:
            print(f"Woop woop 🎉")


@main.command()
@click.option("--language", default="python3")
@click.argument("problem")
def get(problem, language):
    """This command downloads a kattis problem and test files"""
    hostname = (
        cfg.get("active_org")
        if cfg.get("active_org") is not None
        else "open.kattis.com"
    )
    res = requests.get(
        f"https://{hostname}/problems/{problem}/file/statement/samples.zip"
    )

    language_config = language_detector.get_config(language)

    if res.status_code == 404:
        print(
            f"Couldn't find problem '{problem}'. Maybe you typed it wrong? Or no test files exist"
        )
    else:
        print("Downloading samples")
        tmp_file = tempfile.NamedTemporaryFile(delete=False)
        open(tmp_file.name, "wb").write(res.content)

        with zipfile.ZipFile(tmp_file.name, "r") as zip_ref:
            zip_ref.extractall(f"./{problem}")
            print(f"Samples downloaded to './{problem}'")
        tmp_file.close()
        os.unlink(tmp_file.name)

        # Create main.xx with template
        if not os.path.exists(f"./{problem}/solution.{language_config.file_extension}"):
            open(f"./{problem}/solution.{language_config.file_extension}", "w").write(
                language_config.default_content
            )

        if "additional_files" in dir(language_config):
            for file in language_config.additional_files:
                if not os.path.exists(f"./{problem}/{file}"):
                    open(f"./{problem}/{file}", "w").write(
                        language_config.additional_files[file]
                    )

        if "additional_files_that_shouldnt_be_submitted" in dir(language_config):
            for file in language_config.additional_files_that_shouldnt_be_submitted:
                if not os.path.exists(f"./{problem}/{file}"):
                    os.remove(f"./{problem}/{file}")


@main.command()
@click.argument("problem")
def submit(problem):
    """This command submits a problem to kattis"""
    lang = language_detector.determine_language(problem)
    lang_config = language_detector.get_config(lang)
    f = f"./{problem}/solution.{lang_config.file_extension}"

    sub_files = []
    with open(f) as sub_file:
        sub_files.append(
            (
                "sub_file[]",
                (os.path.basename(f), sub_file.read(), "application/octet-stream"),
            )
        )

    if "additional_files" in dir(lang_config):
        for file_name in lang_config.additional_files:
            f = f"./{problem}/{file_name}"
            with open(f) as sub_file:
                sub_files.append(
                    (
                        "sub_file[]",
                        (
                            os.path.basename(f),
                            sub_file.read(),
                            "application/octet-stream",
                        ),
                    )
                )

    submit_problem(problem, sub_files)


@main.group()
def org():
    """Change organization settings"""
    pass


@org.command()
@click.argument("organization", required=False)
def current(organization):
    """Gets or sets the organization"""
    if not organization:
        print("Current org is", cfg.get("active_org") or "open.kattis.com")
    elif cfg.sectionExists(organization) or organization == "open.kattis.com":
        cfg.set("active_org", organization)
        print(f"Changed active org to {organization}")
    else:
        print("You haven't added this organization. Add it with\nkk org add")


@org.command()
def add():
    """Add a new organization"""
    hostname = click.prompt("Organization url", type=str, default="open.kattis.com")
    res = requests.get(f"https://{hostname}")
    if res.status_code == 404:
        print(f"Couldn't find org ({res.request.url}). Did you spell it correctly?")
        return

    print("\n\nNow you need to download the configuration file from the following url:")
    print(f"https://{hostname}/download/kattisrc\n\n")

    username = click.prompt("Kattis username (copy from .kattisrc)", type=str)

    res = requests.get(f"https://{hostname}/users/{username}")
    if res.status_code == 404:
        print(f"Couldn't find user ({res.request.url}). Did you spell it correctly?")
        return

    token = click.prompt("Kattis token (copy from .kattisrc)", type=str)

    cfg.set("username", username, hostname)
    cfg.set("token", token, hostname)


if __name__ == "__main__":
    main()
