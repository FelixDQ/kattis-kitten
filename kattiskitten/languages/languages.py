import glob
import re
import kattiskitten.languages.python3.config as python3_config

SUPPORTED_LANGUAGES = ["python3", "java"]

LANGUAGE_EXTENSIONS = {".py": "python3"}


def get_config(language):
    if language == "python3":
        return python3_config
    else:
        raise ValueError(
            f"Language not supported. Supported languages are: {', '.join(SUPPORTED_LANGUAGES)}")


def determine_language(problem):
    main = glob.glob(f"./{problem}/main.*")

    if len(main) < 1:
        raise ValueError("Couldn't find any program matching patten (main.*)")
    if len(main) > 1:
        raise ValueError("Found more than one program matching patten (main.*). It currently only supports one")

    m = re.search(r".*(\..+?)$", main[0])

    if m:
        extension = m.group(1)
        language = LANGUAGE_EXTENSIONS[extension]
        if not language:
            raise ValueError(f"Couldn't find supported language with extension {extension}")
        
        return language

