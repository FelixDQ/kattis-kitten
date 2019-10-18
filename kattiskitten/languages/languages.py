import glob
import re
import kattiskitten.languages.python3.config as python3_config
import kattiskitten.languages.java.config as java_config

SUPPORTED_LANGUAGES = ["python3", "java"]

LANGUAGE_EXTENSIONS = {
    ".py": "python3",
    ".java": "java",
}


def get_config(language):
    if language == "python3":
        return python3_config
    if language == "java":
        return java_config

    raise ValueError(f"Language not supported. Supported languages are: {', '.join(SUPPORTED_LANGUAGES)}")


def determine_language(problem):
    solution = glob.glob(f"./{problem}/solution.*")

    if len(solution) < 1:
        raise ValueError("Couldn't find any program matching patten (solution.*)")
    if len(solution) > 1:
        raise ValueError(
            "Found more than one program matching patten (solution.*). It currently only supports one")

    m = re.search(r".*(\..+?)$", solution[0])

    if m:
        extension = m.group(1)
        language = LANGUAGE_EXTENSIONS[extension]
        if not language:
            raise ValueError(
                f"Couldn't find supported language with extension {extension}")

        return language
