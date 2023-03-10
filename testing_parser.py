import os
import re

# function is used to read the files in the repo and
# returns a list of strings represeting the files, each being a string
def read_repo_files(repo_dir):
    file_strings = []
    for file in os.listdir(repo_dir):
        if file.endswith(".cpp"):
            with open(os.path.join(repo_dir, file), "r") as f:
                file_string = f.read()
                file_strings.append(file_string)
        elif file.endswith(".java"):
            with open(os.path.join(repo_dir, file), "r") as f:
                file_string = f.read()
                file_strings.append(file_string)
        elif file.endswith(".py"):
            with open(os.path.join(repo_dir, file), "r") as f:
                file_string = f.read()
                file_strings.append(file_string)
    return file_strings


#detects if a function has a docstring
def has_docstring(code):
    if isinstance(code, str):
        if code.startswith("def"):
            # Python function
            match = re.search(r'"""(.*?)"""', code, re.DOTALL)
            return bool(match)
        elif code.startswith("/**"):
            # Java function
            match = re.search(r'/\*\*(.*?)\*/', code, re.DOTALL)
            return bool(match)
        elif code.startswith("//") or code.startswith("/*"):
            # C++ function with special comments
            match = re.search(r'\/\/\!(.*?)\n', code, re.DOTALL)
            return bool(match)
    return False

#function takes a pandas data frame and returns a list of docstrings
def extract_docstrings(df):
    docstrings = []
    for code in df["Code"]:
        if isinstance(code, str):
            if code.startswith("def"):
                # Python function
                match = re.search(r'"""(.*?)"""', code, re.DOTALL)
                if match:
                    docstrings.append(match.group(1))
                else:
                    docstrings.append("")
            else:
                docstrings.append("")
        else:
            docstrings.append("")
    return docstrings

#function takes a pandas data frame and returns a list of unique values in a column
def get_unique_values(df, column_name):
    values = df[column_name].unique().tolist()
    return values
