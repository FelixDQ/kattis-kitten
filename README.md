# Kattis kitten
![Repo size](https://img.shields.io/github/repo-size/FelixDQ/kattis-kitten)
[![PyPI version](https://img.shields.io/pypi/v/kattiskitten)](https://pypi.org/project/kattiskitten/)
[![License](https://img.shields.io/pypi/l/kattiskitten)](https://pypi.org/project/kattiskitten/)

Kattis CLI - Easily download, test and submit kattis problems
```
Usage: kk [OPTIONS] COMMAND [ARGS]...

  Simple CLI for downloading and testing kattis problems

Options:
  --help  Show this message and exit.

Commands:
  get       This command downloads a kattis problem and test files
  problems  Simply opens https://open.kattis.com/problems in your webbrowser
  submit    This command submits a problem to kattis
  test      This tests a kattis problem using provided test problems
```
Installation (requires python >= 3.6):
```
pip3 install kattiskitten
```

# Commands
Download test files.
```
> kk get rationalsequence
Downloading samples
Samples downloaded to './rationalsequence'
```

Test the problem
```
> kk test rationalsequence
👷‍ Testing rationalsequence...
👷‍ Language = Python 3 🐍

🔎 Test number 1:
❌ Failed...
__________INPUT____________
5
1 1/1
2 1/3
3 5/2
4 2178309/1346269
5 1/10000000

__________INPUT____________
__________OUTPUT___________
Hello world!

__________OUTPUT___________
__________EXPECTED_________
1 1/2
2 3/2
3 2/5
4 1346269/1860498
5 10000000/9999999

__________EXPECTED_________
```

Submit solution to kattis
```
> kk submit rationalsequence
Submission received. Submission ID: 5030066.
* Opens web browser on submission page *
```
# Choose language
The default language is python3. To change language you can use the `--language` flag on the get command.
```
> kk get rationalsequence --language java
Downloading samples
Samples downloaded to './rationalsequence'
```
The other commands will auto detect which language you have chosen.

# Supported languages
* Python3
* Java
* Contribute by adding [more languages](https://github.com/FelixDQ/kattis-kitten/tree/master/kattiskitten/languages)! :-) 
