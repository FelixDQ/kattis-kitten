import glob
import subprocess
import colorful as cf
import kattiskitten.language_detector as language_detector
import time

def test_problem(problem, log=True):
    if log: print(f"👷‍ Testing {problem}...")

    lang = language_detector.determine_language(problem)
    lang_config = language_detector.get_config(lang)
    if log: print(f"👷‍ Language = {lang_config.kattis_name} {lang_config.emoji}\n")

    inputs = glob.glob(f"./{problem}/*.in")

    count = 0
    failed = False
    for input in inputs:
        count += 1
        if log:
            print(f"🔎 Test number {count}:")

        input_file = open(input, "rb")
        input_content = input_file.read()

        program_path = f"./{problem}/solution.{lang_config.file_extension}"
        start = time.time()
        output_string = lang_config.run_program(program_path, input_content)
        end = time.time()
        answer = input[:-3] + ".ans"
        answer_file = open(answer, "r")
        answer_content = answer_file.read()

        if output_string.replace("\r\n", "\n") != answer_content.replace("\r\n", "\n"):
            if log:
                print(cf.bold_red("❌ Failed..."))
                print("__________INPUT____________")
                print(input_content.decode('utf-8'))
                print("__________INPUT____________")
                print(cf.red("__________OUTPUT___________"))
                print(cf.red(output_string))
                print(cf.red("__________OUTPUT___________"))
                print("__________EXPECTED_________")
                print(answer_content)
                print("__________EXPECTED_________")

            failed = True
        elif log:
            print(cf.bold_green(f"✅ Test succesful! (completed in {end-start} seconds)\n"))



    return not failed