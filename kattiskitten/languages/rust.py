import subprocess
import tempfile

kattis_name = "Rust"
file_extension = "rs"
emoji = "⚙️"
default_content = """
fn main() {
    println!("Hello, world!");
}
"""
main_class = "solution.rs"


def run_program(file, input_content):
    # Make temporary path
    dirpath = tempfile.mkdtemp()
    subprocess.call(["rustc", file, "-o", dirpath + "/main", "-A", "warnings"])

    try:
        output = subprocess.check_output([dirpath + "/main"], input=input_content)
        return output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        return e.output.decode(
            "utf-8"
        )  # We still want the output when programs exits with an error
