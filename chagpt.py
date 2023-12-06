import os
import pyperclip


def compile_python_files(directory):
    compiled_code = ""

    for filename in os.listdir(directory):
        if filename.endswith(".py") and filename != "chagpt.py":
            with open(os.path.join(directory, filename), "r") as file:
                file_code = file.read()
                compiled_code += f"\n\n`\n{filename}`\n\n```python\n{file_code}\n```"

    return compiled_code


def compile_html_files(directory):
    compiled_code = ""

    for filename in os.listdir(directory):
        if filename.endswith(".html"):
            with open(os.path.join(directory, filename), "r") as file:
                file_code = file.read()
                compiled_code += f"\n\n`{filename}`\n\n```html\n{file_code}\n```"

    return compiled_code


if __name__ == "__main__":
    current_directory = os.getcwd()
    print("Current Directory:", current_directory)
    python_directory = current_directory
    html_directory = f"{current_directory}/templates"

    compiled_python_code = compile_python_files(python_directory)
    compiled_html_code = compile_html_files(html_directory)
    compiled_code = compiled_python_code + compiled_html_code

    # Copy the compiled code to the clipboard
    pyperclip.copy(compiled_code)

    print("Compiled code has been copied to the clipboard.")
