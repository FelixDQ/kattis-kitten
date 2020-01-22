import subprocess
import tempfile

kattis_name = "Java"
file_extension = "java"
emoji = "☕️"
default_content = """class Solution 
{ 
    public static void main(String args[]) 
    { 
        System.out.println("Hello, World"); 
    } 
}
"""
main_class = "Solution"

def run_program(file, input_content):
    # Make temporary path
    dirpath = tempfile.mkdtemp()
    subprocess.call(['javac', file, '-d', dirpath])

    try:
        output = subprocess.check_output(['java', '-cp', dirpath, 'Solution'], input=input_content)
        return output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        return e.output.decode("utf-8") # We still want the output when programs exits with an error