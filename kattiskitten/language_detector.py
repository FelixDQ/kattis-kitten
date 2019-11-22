import glob
import re
import pkgutil
import kattiskitten.languages as languages

SUPPORTED_LANGUAGES = []
LANGUAGE_EXTENSIONS = {}
CONFIGS = {}

for importer, language, ispkg in pkgutil.iter_modules(languages.__path__):
    SUPPORTED_LANGUAGES.append(language)
    config = importer.find_module(language).load_module(language)

    LANGUAGE_EXTENSIONS[config.file_extension] = language
    CONFIGS[language] = config

def get_config(language):
    if language not in CONFIGS:
        raise ValueError(f"Language not supported. Supported languages are: {', '.join(SUPPORTED_LANGUAGES)}")
    return CONFIGS[language]



def determine_language(problem):
    solution = glob.glob(f"./{problem}/solution.*")

    if len(solution) < 1:
        raise ValueError("Couldn't find any program matching patten (solution.*)")
    if len(solution) > 1:
        raise ValueError(
            "Found more than one program matching patten (solution.*). It currently only supports one")

    m = re.search(r".*\.(.+?)$", solution[0])

    if m:
        extension = m.group(1)
        language = LANGUAGE_EXTENSIONS[extension]
        if not language:
            raise ValueError(
                f"Couldn't find supported language with extension {extension}")

        return language
