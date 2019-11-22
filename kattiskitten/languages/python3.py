import subprocess

kattis_name = "Python 3"
file_extension = "py"
default_content = 'print("Hello world!")'
emoji = "🐍"
main_class = "solution.py"

def run_program(file, input_content):
    try:
        output = subprocess.check_output(['python3', file], input=input_content)
        return output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        return e.output.decode("utf-8") # We still want the output when programs exits with an error