
import requests
from bs4 import BeautifulSoup

def get_problem_score(problem):
    res = requests.get(f"https://open.kattis.com/problems/{problem}")
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, features="html.parser")
        difficulity_title = soup.find('strong', text="Difficulty:  ")
        return float(difficulity_title.find_next_sibling("span").text)
    return 0