import subprocess
import tempfile
import os

kattis_name = "C"
file_extension = "c"
emoji = "👻"
default_content = """#include <stdio.h>
int main() {
   printf("Hello, World!");
   return 0;
}
"""
main_class = "solution.c"

def run_program(file, input_content):
    # Make temporary path
    dirpath = tempfile.mkdtemp()
    compiled_path = os.path.join(dirpath, 'program')
    subprocess.call(['gcc', file, '-o', compiled_path])

    try:
        output = subprocess.check_output([compiled_path], input=input_content)
        return output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        return e.output.decode("utf-8") # We still want the output when programs exits with an error