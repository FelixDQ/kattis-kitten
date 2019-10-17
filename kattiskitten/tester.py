import glob
import subprocess
import colorful as cf

def test_problem(problem, log=True):
    if log:
        print(f"👷‍ Testing {problem}:\n")
    inputs = glob.glob(f"./{problem}/*.in")

    count = 0
    for input in inputs:
        count += 1
        if log:
            print(f"🔎 Test number {count}:")

        input_file = open(input, "rb")
        input_content = input_file.read()

        output_string = None
        try:
            output = subprocess.check_output(
                ['python3', f"./{problem}/main.py"], input=input_content)
            output_string = output.decode("utf-8")
        except subprocess.CalledProcessError as e:
            output_string = e.output.decode("utf-8")

        answer = input.replace('.in', '.ans')
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

            return False
        elif log:
            print(cf.bold_green("✅ Test succesful!\n"))



    return True