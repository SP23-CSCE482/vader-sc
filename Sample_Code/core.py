"""Koninklijke Philips N.V., 2019 - 2020. All rights reserved."""

import datetime
import fnmatch
import subprocess
import os
import re
import sys
import time
import pprint

import pandas as pd
import extractor_log as cl

LOG = cl.get_logger()
DELTA_BODY = []
UID_LIST = []
FILE_TYPE = ["JAVA", "CPP", "C", "CS", "PY", "TS", "JS"]  # pragma: no mutate


# Generated: Function used for getting all the valid file names from the given directory
# Generated: Function used for getting all the valid file names from the given directory
# Generated: Function used for getting all the valid file names from the given directory
# Generated: Function used for getting all the valid file names from the given directory
def get_file_names(dir_path):
    """ Function used for getting all the valid file names from the given directory
        @parameters
        dir_path: Path to the repository
        @return
        This function returns all the files in the given directory"""
    path_list = [os.path.join(dirpath, filename) for dirpath, _, filenames in
                 os.walk(dir_path) for filename in filenames]
    return path_list


# Generated: Function used to filter requested file patterns from the files in the given directory
# Generated: Function used to filter requested file patterns from the files in the given directory
# Generated: Function used to filter requested file patterns from the files in the given directory
# Generated: Function used to filter requested file patterns from the files in the given directory
def filter_reg_files(allfiles, reg_pattern):
    """ Function used to filter requested file patterns
        from the files in the given directory
        @parameters
        allfiles: list of all files in the repository
        @return
        This function returns filtered files in the given directory"""
    cmd = ""  # pragma: no mutate
    regex, filtered_files = [], []
    if reg_pattern is None:
        filtered_files = allfiles
    else:
        reg_pattern = reg_pattern.split(",")
        for i in range(len(reg_pattern).__trunc__()):
            cmd = "{} " + cmd  # pragma: no mutate
            regex.append(fnmatch.translate(reg_pattern[i]))
        cmd = "(" + cmd[:-1].replace(" ", "|") + ")"  # pragma: no mutate
        re_obj = re.compile(cmd.format(*regex))
        [filtered_files.append(allfiles[i]) if
         re.match(re_obj, allfiles[i]) is None else None for i in range(len(allfiles))]
    return filtered_files


# Generated: Function to execute ctags command
# Generated: Function to execute ctags command
# Generated: Function to execute ctags command
# Generated: Function to execute ctags command
def run_ctags_cmd(file_ext, file_names, find):
    """ Function to execute ctags command
        @parameters
        file_ext: file type(.py, .java etc)
        file_names: path to file
        find: keyword to run ctags command
        @return
        This function returns ctags output"""
    if file_ext.upper() == "PY":
        cmd = 'ctags -x "%s"' % file_names  # pragma: no mutate
    elif file_ext.upper() in ["TS", "JS"]:  # pragma: no mutate
        cmd = 'ctags --language-force=java -x "%s" | grep %s' % (file_names, find)  # pragma: no mutate
    else:
        cmd = 'ctags -x "%s" | grep %s' % (file_names, find)  # pragma: no mutate
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    return proc


# Generated: Function to get method/function names from the input files in the given repository.
# Generated: Function to get method/function names from the input files in the given repository.
# Generated: Function to get method/function names from the input files in the given repository.
# Generated: Function to get method/function names from the input files in the given repository.
def get_function_names(file_names, ignoreDocumented):
    """ Function to get method/function names from the input files in the given repository
        @parameters
        file_names: Path to the file
        @return
        This function returns function/method names and line numbers of all the given files"""
    file_ext = file_names.split('.')[-1].upper()
    find = "function" if file_ext.upper() == "CPP" or file_ext.upper() == "C" \
        else ["member", "function", "class"] if file_ext.upper() == "PY" else "method"  # pragma: no mutate
    proc = run_ctags_cmd(file_ext, file_names, find)
    process = str(proc.stdout.read(), 'utf-8')  # pragma: no mutate
    return process_function_names(process, find, file_names, ignoreDocumented)


# Generated: This function cleans the ctags output to get function/method names and line numbers
# Generated: This function cleans the ctags output to get function/method names and line numbers
# Generated: This function cleans the ctags output to get function/method names and line numbers
# Generated: This function cleans the ctags output to get function/method names and line numbers
def process_function_names(func_data, find, file_name, ignoreDocumented):
    """ This function cleans the ctags output to get function/method names and line numbers
        @parameters
        func_data: Ctags output
        find: keyword of method type(member/function/class/method)
        @return
        This function returns list of function names and line numbers"""
    if func_data is not None:
        process_list = re.findall(r'\w+', func_data)
        if find == ["member", "function", "class"]:  # pragma: no mutate
            val = [index for index, _ in enumerate(process_list) if
                   process_list[index - 1] in find and process_list[index].isdigit()]
        else:
            val = process_ctags_output(find, process_list)
        function_list = get_sorted_func_list(process_list, val)
        line_numbers = get_func_line_num_list(process_list, val)
        line_numbers.sort()

        final_func_list = []
        final_num_list = []
        if(ignoreDocumented):
            commented_functions_boolean_list = list_commented_function(line_numbers, file_name)
            for i in range(len(commented_functions_boolean_list)):
                if(not commented_functions_boolean_list[i]):
                    final_func_list.append(function_list[i])
                    final_num_list.append(line_numbers[i])
        else:
            final_func_list = function_list
            final_num_list = line_numbers
    else:
        print("Input files doesn't have valid methods")  # pragma: no mutate
        sys.exit(1)  # pragma: no mutate
    return final_func_list, final_num_list


# Given a list of line numbers, check if each function has been commented.
# Returns a list of booleans, True = commented, False = not commented
# Generated: returns list of comments (or commented functions)
# Generated: returns list of comments (or commented functions)
# Generated: returns list of comments (or commented functions)
# Generated: returns list of comments (or commented functions)
def list_commented_function(line_num_list, file_name):
    file_ext = file_name.split('.')[-1].upper()

    commentSymbols = ['#']
    if(file_ext == "CPP" or file_ext =="C"):
        commentSymbols = ['//', '/*', '*/']

    is_commented_list = [False for i in range (len(line_num_list))]
    index = 0
    with open(file_name, 'r') as fp:
        for i, line in enumerate(fp):
            if (i + 2) == line_num_list[index] :
                if any(symbol in line for symbol in commentSymbols):
                    is_commented_list[index] = True;
            elif (i + 1) == line_num_list[index]:
                if any(symbol in line for symbol in commentSymbols):
                    is_commented_list[index] = True;
                index +=1
                if(index >= len(line_num_list)):
                    break;
                if(line_num_list[index] <= i):
                    index +=1

    return is_commented_list


# Generated: This function cleans the ctags output to get function/method names and line numbers find: keyword of method type(member/function/class/method) process_list: list of function names and line numbers
# Generated: This function cleans the ctags output to get function/method names and line numbers find: keyword of method type(member/function/class/method) process_list: list of function names and line numbers
# Generated: This function cleans the ctags output to get function/method names and line numbers find: keyword of method type(member/function/class/method) process_list: list of function names and line numbers
# Generated: This function cleans the ctags output to get function/method names and line numbers find: keyword of method type(member/function/class/method) process_list: list of function names and line numbers
def process_ctags_output(find, process_list):
    """ This function cleans the ctags output to get function/method names and line numbers
        @parameters
        process_list: Ctags output in list format
        find: keyword of method type(member/function/class/method)
        @return
        This function returns list of function names and line numbers"""
    return [index for index, _ in enumerate(process_list) if
            process_list[index - 1] == find and process_list[index].isdigit()]


# Generated: This function sorts function names with respective to line numbers and returns list of sorted function names based on line numbers
# Generated: This function sorts function names with respective to line numbers and returns list of sorted function names based on line numbers
# Generated: This function sorts function names with respective to line numbers and returns list of sorted function names based on line numbers
# Generated: This function sorts function names with respective to line numbers and returns list of sorted function names based on line numbers
def get_sorted_func_list(process_list, val):
    """ This function sorts function names with respective to line numbers
        @parameters
        process_list: Ctags output in list format
        val: filtered variable to get function name
        @return
        This function returns list of sorted function names based on line numbers"""
    return [val for _, val in
            sorted(zip(get_func_line_num_list(process_list, val), get_func_list(process_list, val)))]


# Generated: This function refines the ctags output to get function names
# Generated: This function refines the ctags output to get function names
# Generated: This function refines the ctags output to get function names
# Generated: This function refines the ctags output to get function names
def get_func_list(process_list, val):
    """ This function refines the ctags output to get function names
        @parameters
        process_list: Ctags output in list format
        val: filtered variable to get function name
        @return
        This function returns list of function"""
    function_list = []
    [function_list.append(process_list[val[i] - 2]) for i in range(len(val))]
    return function_list


# Generated: This function refines the ctags output to get function line numbers
# Generated: This function refines the ctags output to get function line numbers
# Generated: This function refines the ctags output to get function line numbers
# Generated: This function refines the ctags output to get function line numbers
def get_func_line_num_list(process_list, val):
    """ This function refines the ctags output to get function line numbers
        @parameters
        process_list: Ctags output in list format
        val: filtered variable to get function name
        @return
        This function returns list of function line numbers"""
    line_numbers = []
    [line_numbers.append(int(process_list[val[i]])) for i in range(len(val))]
    return line_numbers


# Generated: Function checks for the given annotation condition
# Generated: Function checks for the given annotation condition
# Generated: Function checks for the given annotation condition
# Generated: Function checks for the given annotation condition
def check_annot(filename, line_num, annot, removeCppSignatures):
    """ Function checks for the annotation condition
        @parameters
        filename: Path to the file
        line_num: function/method line number
        annot: Annotation condition (Ex: @Test)
        @return
        This function returns function/method definitions that has the given annotation"""
    ret_val = None
    if annot is None:
        ret_val = get_func_body(filename, line_num, removeCppSignatures)
    else:
        ret_val = get_annot_methods(filename, line_num, annot)
    return ret_val


# Generated: Function reads the given file and returns the content of the file inputed
# Generated: Function reads the given file and returns the content of the file inputed
# Generated: Function reads the given file and returns the content of the file inputed
# Generated: Function reads the given file and returns the content of the file inputed
def get_file_content(filename):
    """ Function reads the given file
        @parameters
        filename: Path to the file
        @return
        This function returns content of the file inputed"""
    with open(filename, encoding='utf-8', errors='ignore') as file_data:  # pragma: no mutate
        return file_data.readlines()


# Generated: This function gets the methods that have given annotation This function returns function/method definitions that have the given annotation
# Generated: This function gets the methods that have given annotation This function returns function/method definitions that have the given annotation
# Generated: This function gets the methods that have given annotation This function returns function/method definitions that have the given annotation
# Generated: This function gets the methods that have given annotation This function returns function/method definitions that have the given annotation
def get_annot_methods(filename, line_num, annot):
    """ This function gets the methods that have given annotation
        @parameters
        filename: Path to the file
        line_num: function/method line number
        annot: Annotation condition (Ex: @Test)
        @return
        This function returns function/method definitions that has the given annotation"""
    file_content = get_file_content(filename)
    iterator = int(line_num) - 2  # Iterating through lines to check for annotations
    try:
        for _ in range(int(line_num) - 2):  # pragma: no mutate
            data = str(file_content[iterator]).strip()
            iterator = iterator - 1
            ret_val = process_annot_method_body(annot, data, filename, line_num)
            if ret_val != "continue":  # pragma: no mutate
                return ret_val
    except IndexError as exc:
        LOG.info("error while processing file_line: %s", filename + "_" + line_num)  # pragma: no mutate
        LOG.info(exc)  # pragma: no mutate


# Generated: This function process the annotation to extract methods having given annotation
# Generated: This function process the annotation to extract methods having given annotation
# Generated: This function process the annotation to extract methods having given annotation
# Generated: This function process the annotation to extract methods having given annotation
def process_annotation(annot):
    """ This function process the annotation to extract methods having given annotation
            @parameters
            annot: Annotation condition (Ex: @Test)
            @return
            This function returns starting and ending character of the annotation"""
    annot_start = annot[0]
    annot_end = annot[len(annot) - 1]
    if annot_end.isalpha():
        annot_end = None  # pragma: no mutate
    return annot_start, annot_end


# Generated: Process the body of a function/method annotation
# Generated: Process the body of a function/method annotation
# Generated: Process the body of a function/method annotation
# Generated: Process the body of a function/method annotation
def process_annot_method_body(annot, data, filename, line_num):
    """ This function process the function/method to check if it has the given annotation
        @parameters
        filename: Path to the file
        line_num: function/method line number
        annot: Annotation condition (Ex: @Test)
        data: Content of the given file
        @return
        This function returns function/method definitions that has the given annotation"""
    ret_val = "continue"  # pragma: no mutate
    annot_start, annot_end = process_annotation(annot)
    if annot.strip(annot_start).strip(annot_end).upper() in data.strip(annot_start) \
            .strip(annot_end).upper().split(",") and data.strip().startswith(annot_start):
        body = get_func_body(filename, line_num)
        if body is None:
            body = ""  # pragma: no mutate
        ret_val = data + os.linesep + str(body)
    elif data[:1] != "@" and str(data).strip() == "}" or str(data).strip() == "{":  # pragma: no mutate
        ret_val = None  # pragma: no mutate
    return ret_val


# Generated: Function checks for the annotation condition in python files.
# Generated: Function checks for the annotation condition in python files.
# Generated: Function checks for the annotation condition in python files.
# Generated: Function checks for the annotation condition in python files.
def check_py_annot(file_name, annot):
    """ Function checks for the annotation condition in python files
        @parameters
        filename: Path to the file
        annot: Annotation condition (Ex: @Test)
        @return
        This function returns function/method names that has the given annotation"""
    line_data = list(
        [line.rstrip() for line in open(file_name, encoding='utf-8', errors='ignore')])  # pragma: no mutate
    val = 1  # pragma: no mutate
    if annot[0] != "@":  # Making use of annotation search function for function start with feature too
        annot = "def " + annot.lower()  # pragma: no mutate
        val = -1  # pragma: no mutate
    return get_py_annot_method_names(line_data, annot, val)


# Generated: Function checks for the annotation condition in python files and returns function/method names that has the given annotation
# Generated: Function checks for the annotation condition in python files and returns function/method names that has the given annotation
# Generated: Function checks for the annotation condition in python files and returns function/method names that has the given annotation
# Generated: Function checks for the annotation condition in python files and returns function/method names that has the given annotation
def get_py_annot_method_names(line_data, annot, val):
    """ Function checks for the annotation condition in python files
        @parameters
        line_data: File content in list format
        annot: Annotation condition (Ex: @Test)
        val: index pointer that helps in getting method name
        @return
        This function returns function/method names that has the given annotation"""
    data = []
    for i, _ in enumerate(line_data):
        if annot in line_data[i]:
            if str(line_data[i]).strip().split(" ")[0] == "def":  # pragma: no mutate
                func_name = line_data[i + 1 + val].strip().split(" ")[1].split("(")[0]  # pragma: no mutate
                data.append(func_name)
            else:
                for j in range(i, len(line_data)):
                    if str(line_data[j]).strip().split(" ")[0] == "def":  # pragma: no mutate
                        func_name = line_data[j].strip().split(" ")[1].split("(")[0]  # pragma: no mutate
                        data.append(func_name)
                        break
    return data


# Generated: Function to get method/function body from files
# Generated: Function to get method/function body from files
# Generated: Function to get method/function body from files
# Generated: Function to get method/function body from files
def get_func_body(filename, line_num, removeCppSignatures):
    """ Function to get method/function body from files
        @parameters
        filename, line_num: Path to the file, function/method line number
        @return
        This function returns function/method definitions of all the given files"""
    line_num = int(line_num)
    code = ""  # pragma: no mutate
    cnt_braket = 0
    found_start = False
    return_val = None
    with open(filename, "r", encoding='utf-8', errors='ignore') as files:  # pragma: no mutate
        for i, line in enumerate(files):
            if i >= (line_num - 1):
                code += line

                if line.count("{") > 0:
                    found_start = True
                    cnt_braket += line.count("{")

                if line.count("}") > 0:
                    cnt_braket -= line.count("}")

                if cnt_braket == 0 and found_start is True:
                    return_val = code
                    break
    if filename.split('.')[-1].upper() == "CPP" and removeCppSignatures:
        nameEndIndex = return_val.find('(')
        functionSignatureSubstring = return_val[0:nameEndIndex]
        reversedFunctionSignatureSubstring = functionSignatureSubstring[::-1]
        index = re.search(r'\W+', reversedFunctionSignatureSubstring).start()
        func_name = reversedFunctionSignatureSubstring[0:index][::-1]
        return_val = func_name + return_val[nameEndIndex:]

    return return_val


# Generated: Function to get method/function body from files
# Generated: Function to get method/function body from files
# Generated: Function to get method/function body from files
# Generated: Function to get method/function body from files
def get_py_func_body(line_numbers, file_name, annot):
    """ Function to get method/function body from files
        @parameters
        filename: Path to the file
        line_numbers: function/method line number
        annot: Annotation condition (Ex: @Test)
        @return
        This function returns python function/method definitions and line_numbers in the given files"""
    func_name = []
    func_body = []
    line_data = list([line.rstrip() for line
                      in open(file_name, encoding='utf-8', errors='ignore')])  # pragma: no mutate
    data, data_func_name, final_numbers = process_py_methods(file_name, line_numbers, line_data)
    if annot is not None:
        data_func_name, data = get_py_annot_methods(file_name, data_func_name, data, annot)
    if len(data_func_name).__trunc__() != 0:
        func_name, func_body = process_py_func_body(data, data_func_name)
    return func_name, func_body, final_numbers


def process_py_methods(file_name, line_numbers, line_data):
    """ This Function refines the python function names to remove any class or lamida functions
        @parameters
        filename: Path to the file
        line_num: function/method line number
        line_data: File content in list format
        @return
        This function returns processed python function/method names, definitions, line numbers in the given files"""
    data = []
    data_func_name = []
    final_numbers = []
    for i, _ in enumerate(line_numbers):
        start = line_numbers[i]
        stop = len(line_data) if i == len(line_numbers) - 1 else line_numbers[i + 1] - 1
        data.append(os.linesep.join(line_data[start - 1:stop]))  # pragma: no mutate
        data_func_name.append(str(file_name) + "_" + str(line_data[start - 1].strip().split(" ")[1].split("(")[0]))
        if data[len(data) - 1].startswith("class") or "lambda" in data[len(data) - 1]:
            data.remove(data[len(data) - 1])
            data_func_name.pop(len(data_func_name) - 1)
            continue
        final_numbers.append(line_numbers[i])
    return data, data_func_name, final_numbers


# Generated: This function filters the python functions to get methods that have given annotation This function returns python function/method names and definitions that have the given annotation
# Generated: This function filters the python functions to get methods that have given annotation This function returns python function/method names and definitions that have the given annotation
# Generated: This function filters the python functions to get methods that have given annotation This function returns python function/method names and definitions that have the given annotation
# Generated: This function filters the python functions to get methods that have given annotation This function returns python function/method names and definitions that have the given annotation
def get_py_annot_methods(file_name, data_func_name, data, annot):
    """ This function filters the python functions to get methods that have given annotation
        @parameters
        filename: Path to the file
        data_func_name: list of all function names in the file
        data: File content in list format
        annot: Annotation condition (Ex: @staticmethod)
        @return
        This function returns python function/method names and definitions that have the given annotation"""
    annot_meth_line_num = check_py_annot(file_name, annot)
    annot_meth_name = []
    annot_meth_body = []
    for k, _ in enumerate(annot_meth_line_num):
        for j, _ in enumerate(data_func_name):
            if str(annot_meth_line_num[k]) in str(data_func_name[j]):
                annot_meth_body.append(data[j])
                annot_meth_name.append(data_func_name[j])
                break
    return annot_meth_name, annot_meth_body


# Generated: This function processes the collected python function definitions to put then in a organized way This function returns python function/method definitions in a organized format
# Generated: This function processes the collected python function definitions to put then in a organized way This function returns python function/method definitions in a organized format
# Generated: This function processes the collected python function definitions to put then in a organized way This function returns python function/method definitions in a organized format
# Generated: This function processes the collected python function definitions to put then in a organized way This function returns python function/method definitions in a organized format
def process_py_func_body(data_body, data_name):
    """ This function processes the collected python function definitions to put then in a organized way
        @parameters
        data_body: list of all function definitions in the file
        data_name: list of all function names in the file
        @return
        This function returns python function/method definitions in a organized format"""
    for i, _ in enumerate(data_body):
        data_body[i] = os.linesep.join([s for s in str(data_body[i]).splitlines() if s])  # pragma: no mutate
    data_body = clean_py_methods(data_body)
    return data_name, data_body


# Generated: This function cleans the collected python function definitions to remove any junk content entered into method while collecting
# Generated: This function cleans the collected python function definitions to remove any junk content entered into method while collecting
# Generated: This function cleans the collected python function definitions to remove any junk content entered into method while collecting
# Generated: This function cleans the collected python function definitions to remove any junk content entered into method while collecting
def clean_py_methods(data_body):
    """ This function cleans the collected python function definitions to remove any junk content entered into method
        while collecting
        @parameters
        data_body: list of all function definitions in the file
        data_name: list of all function names in the file
        @return
        This function returns python function/method definitions in a organized format"""
    for j, _ in enumerate(data_body):
        data_list = list(str(data_body[j]).split(os.linesep))
        count = len(data_list[0]) - len(data_list[0].lstrip())
        i = 0  # pragma: no mutate
        for i, _ in enumerate(data_list):
            if i == len(data_list) - 1 or len(data_list[i + 1]) \
                    - len(data_list[i + 1].lstrip()) <= count:  # pragma: no mutate
                break
        del data_list[i + 1:]
        data_body[j] = str(os.linesep.join(data_list))
    return data_body


# Generated: Function to filter required files from list of all files
# Generated: Function to filter required files from list of all files
# Generated: Function to filter required files from list of all files
# Generated: Function to filter required files from list of all files
def filter_files(list_files):
    """ Function to filter required files from list of all files
    @parameters
    list_files: List of all files that the given repository contains
    @return
    This function returns the list of required file(.java, .cpp, .c, .cs, .py) paths """
    local_files = []
    for files in list_files:
        extension = files.split('.')[-1].upper()  # pragma: no mutate
        if len(extension).__trunc__() > 0:
            if extension in FILE_TYPE:
                local_files.append(files)
    return local_files


# Generated: Function to get + and - delta number of lines from the annoted method/function
# Generated: Function to get + and - delta number of lines from the annoted method/function
# Generated: Function to get + and - delta number of lines from the annoted method/function
# Generated: Function to get + and - delta number of lines from the annoted method/function
def get_delta_lines(file_name, annot, delta):
    """ Function to get + and - delta number of lines from the annoted method/function
            @parameters
            filename, annot, delta: Path to the file, required annotation, required lines from method """
    try:
        line_data = list(filter(None, [line.rstrip() for
                                       line in
                                       open(file_name, encoding='utf-8', errors='ignore')]))  # pragma: no mutate
        data = []
        for num, line in enumerate(line_data, 1):
            process_delta_lines_body(annot, line, delta, num, line_data, data, file_name)
            data = []
    except IOError as exc:
        LOG.info("Cannot read file: %s", file_name)  # pragma: no mutate
        LOG.info(exc)  # pragma: no mutate


# Generated: Function to get + and - delta number of lines from the annoted method/function
# Generated: Function to get + and - delta number of lines from the annoted method/function
# Generated: Function to get + and - delta number of lines from the annoted method/function
# Generated: Function to get + and - delta number of lines from the annoted method/function
def process_delta_lines_body(annot, line, delta, num, line_data, data, file_name):
    """ Function to get + and - delta number of lines from the annoted method/function
        @parameters
        file_name: Path to the file
        annot: Required annotation
        delta: Required lines from method
        line_data: File content in list format
        data: variable that holds delta lines data"""
    if annot.upper() in line.strip().upper():
        for i in range(0, (int(delta) * 2) + 1):
            if num - (int(delta) + 1) + i >= len(line_data):  # pragma: no mutate
                break
            data.append(line_data[num - (int(delta) + 1) + i])
        DELTA_BODY.append("\n".join(data))
        UID_LIST.append(os.path.basename(file_name) + "_")


# Generated: Function that generates a list by merging a list of sub lists
# Generated: Function that generates a list by merging a list of sub lists
# Generated: Function that generates a list by merging a list of sub lists
# Generated: Function that generates a list by merging a list of sub lists
def get_flat_list(data_list):
    """ Function that generates a list by merging a list of sub lists
        @parameters
        data_list: list of sub lists
        @return
        This function returns a flattened list"""
    flattened_list = []
    for val in data_list:
        if str(type(val)) != "<class 'list'>":
            flattened_list.append(val)
        if str(type(val)) == "<class 'list'>":
            for sub_val in val:
                flattened_list.append(sub_val)
    return flattened_list


# Generated: This function processes delta lines data to generate a dataframe
# Generated: This function processes delta lines data to generate a dataframe
# Generated: This function processes delta lines data to generate a dataframe
# Generated: This function processes delta lines data to generate a dataframe
def process_delta_lines_data():
    """ This function processes delta lines data to generate a dataframe
        @return
        This function returns a dataframe of delta lines data"""
    data = {'Uniq ID': UID_LIST, 'Code': DELTA_BODY}
    data_frame = pd.DataFrame(data)
    UID_LIST.clear()
    mask = data_frame['Uniq ID'].duplicated(keep=False)
    data_frame.loc[mask, 'Uniq ID'] += data_frame.groupby('Uniq ID').cumcount().add(1).astype(str)
    return data_frame.sort_values('Uniq ID')


# Generated: This function processes function/method data to generate a dataframe
# Generated: This function processes function/method data to generate a dataframe
# Generated: This function processes function/method data to generate a dataframe
# Generated: This function processes function/method data to generate a dataframe
def process_final_data(code_list, line_list):
    """ This function processes function/method data to generate a dataframe
        @params
        code_list: code list
        line_num: line_list
        @return
        This function returns a dataframe of function/method data"""
    flat_uid_list = get_flat_list(UID_LIST)
    flat_code_list = get_flat_list(code_list)
    data = {'Uniq ID': flat_uid_list, 'Code': flat_code_list, 'Line': line_list}
    data_frame = pd.DataFrame.from_dict(data, orient='index')
    data_frame = data_frame.transpose()
    UID_LIST.clear()
    return data_frame


# Generated: This function processes that input python files to extract methods from the given repo.
# Generated: This function processes that input python files to extract methods from the given repo.
# Generated: This function processes that input python files to extract methods from the given repo.
# Generated: This function processes that input python files to extract methods from the given repo.
def process_py_files(code_list, line_nums, line_num, func_name, annot, functionstartwith):
    """ This function processes that input python files to extract methods from the given repo
        @parameters
        code_list: list to store the extracted methods
        line_num: list of function line numbers
        line_nums: list to store line numbers
        func_name: list of function names
        annot: given annotation condition (Ex: @staticmethod)
        @return
        This function returns extracted python methods"""
    if functionstartwith is not None:
        annot = functionstartwith
    if len(line_num).__trunc__() != 0:
        def_name, def_body, final_numbers = get_py_func_body(line_num, func_name, annot)
        if len(def_body).__trunc__() != 0:
            UID_LIST.append(def_name)
            code_list.append(def_body)
            line_nums.extend(final_numbers)
    return code_list, line_nums


# Generated: This function processes that input files to extract methods from the given repo, and stores the extracted methods.
# Generated: This function processes that input files to extract methods from the given repo, and stores the extracted methods.
# Generated: This function processes that input files to extract methods from the given repo, and stores the extracted methods.
# Generated: This function processes that input files to extract methods from the given repo, and stores the extracted methods.
def process_input_files(line_num, line_nums, functions, annot, func_name, code_list, functionstartwith, removeCppSignatures):
    """ This function processes that input files to extract methods from the given repo
        @parameters
        code_list: list to store the extracted methods
        line_num: list of function line numbers
        line_nums: list to store line numbers
        func_name: list of function names
        annot: given annotation condition (Ex: @staticmethod)
        @return
        This function returns extracted python methods and numbers"""
    if functionstartwith is not None:
        filter_func, filer_line_no = [], []
        for i in range(len(line_num).__trunc__()):
            if str(functions[i]).upper().startswith(functionstartwith.upper()):
                filter_func.append(functions[i])
                filer_line_no.append(line_num[i])
        functions = filter_func
        line_num = filer_line_no
    for lin_no, func in zip(line_num, functions):
        if check_annot(func_name, lin_no, annot, removeCppSignatures) is not None:
            code_list.append(check_annot(func_name, lin_no, annot, removeCppSignatures))
            UID_LIST.append(func_name + "_" + func)
            line_nums.append(lin_no)

    return code_list, line_nums


# Generated: This function processes extracted data to generate a dataframe. delta: Required lines from method line_num: List of line numbers
# Generated: This function processes extracted data to generate a dataframe. delta: Required lines from method line_num: List of line numbers
# Generated: This function processes extracted data to generate a dataframe. delta: Required lines from method line_num: List of line numbers
# Generated: This function processes extracted data to generate a dataframe. delta: Required lines from method line_num: List of line numbers
def get_final_dataframe(delta, code_list, line_num):
    """ This function processes extracted data to generate a dataframe
         @parameters
        code_list: list of extracted methods
        delta: Required lines from method
        line_num: List of line numbers
        @return
        This function returns a dataframe of extracted function/methods"""
    if delta is not None:
        ret_val = process_delta_lines_data()
    else:
        ret_val = process_final_data(code_list, line_num)
    return ret_val


# Generated: Function to clean the log file
# Generated: Function to clean the log file
# Generated: Function to clean the log file
# Generated: Function to clean the log file
def clean_log():
    """ Function to clean the log file"""
    ini_path = os.path.abspath(os.path.join
                               (os.path.dirname(__file__), os.pardir))
    file_name = os.path.join(ini_path, "functiondefextractor", "extractor.log")
    if os.path.exists(file_name):
        open(file_name, 'w').close()


# Generated: This function removes comments from the code extracted
# Generated: This function removes comments from the code extracted
# Generated: This function removes comments from the code extracted
# Generated: This function removes comments from the code extracted
def remove_comments(dataframe):
    """ This function removes comments from the code extracted
            @parameters
            dataframe: extracted methods in dataframe format
            @return
            This function returns function/method definitions by removing comments"""
    filtered_code = []
    data = ""
    for i in range(len(dataframe).__trunc__()):
        for line in dataframe.iat[i, 1].splitlines():
            if not line.strip().startswith(("#", "//", "/*", "*", "*/")):  # pragma: no mutate
                data = data + line.strip().split(";")[0] + os.linesep
        filtered_code.append(data)
        data = ""
    dataframe["Code"] = filtered_code
    return dataframe


# Generated: This function classifies the report files based on the file type (Ex:.java,.cs,.py, etc.)
# Generated: This function classifies the report files based on the file type (Ex:.java,.cs,.py, etc.)
# Generated: This function classifies the report files based on the file type (Ex:.java,.cs,.py, etc.)
# Generated: This function classifies the report files based on the file type (Ex:.java,.cs,.py, etc.)
def get_report(data, path):
    """ This function classifies the report files based on the file type(Ex: .java, .cs, .py, etc.)
                @parameters
                data: extracted methods in dataframe format
                path: Report folder path"""
    method_data = [[] for _ in range(len(FILE_TYPE))]
    method_name = [[] for _ in range(len(FILE_TYPE))]
    for i in range(len(data).__trunc__()):
        extension = data["Uniq ID"][i].split('.')[-1].upper()  # pragma: no mutate
        res = str([ext for ext in FILE_TYPE if ext == str(extension).split("_")[0].upper()])  # pragma: no mutate
        if str(res) != "[]":  # pragma: no mutate
            method_data[int(FILE_TYPE.index(res.strip("[]''")))].append(data.iat[i, 1])  # pylint: disable=E1310
            method_name[int(FILE_TYPE.index(res.strip("[]''")))].append(data.iat[i, 0])  # pylint: disable=E1310
    return write_report_files(path, method_name, method_data)


# Generated: This function write the dataframe to excel files
# Generated: This function write the dataframe to excel files
# Generated: This function write the dataframe to excel files
# Generated: This function write the dataframe to excel files
def write_report_files(path, method_name, method_data):
    """ This function write the dataframe to excel files
        @parameters
        path: Report folder path
        method_name: extracted method names
        method_data: extracted method definitions
        @return
        returns a dataframe with all the extracted method names and definitions"""
    for i in range(len(FILE_TYPE).__trunc__()):
        dataframe = pd.DataFrame(list(zip(method_name[i], method_data[i])),
                                 columns=['Uniq ID', 'Code'])
        if len(dataframe).__trunc__() != 0:
            writer = pd.ExcelWriter('%s.xlsx' %  # pragma: no mutate
                                    os.path.join(path, "ExtractedFunc_" + str(FILE_TYPE[i]).strip(  # pragma: no mutate
                                        ".") + "_" + str(datetime.datetime.  # pragma: no mutate
                                                         fromtimestamp(time.time())
                                                         .strftime('%H-%M-%S_%d_%m_%Y'))),  # pragma: no mutate
                                    engine='xlsxwriter')  # pragma: no mutate
            dataframe.to_excel(writer, sheet_name="funcDefExtractResult")
            writer.save()
    return pd.DataFrame(list(zip(method_name, method_data)), columns=['Uniq ID', 'Code'])


# Generated: This function helps in validating the user inputs
# Generated: This function helps in validating the user inputs
# Generated: This function helps in validating the user inputs
# Generated: This function helps in validating the user inputs
def validate_input_paths(path):
    """This function helps in validating the user inputs"""
    ret_val = None
    status_path = os.path.exists(path)
    if status_path:
        ret_val = False
    if not status_path:
        ret_val = True
    return ret_val


# Generated: Function that initializes the input variables
# Generated: Function that initializes the input variables
# Generated: Function that initializes the input variables
# Generated: Function that initializes the input variables
def initialize_values(delta, annot, path_loc, report_folder):
    """ Function that initializes the input variables
            @parameters
            path_loc: directory path of the repository
            annot: given annotation condition (Ex: @staticmethod, @Test)
            report_folder: path to report
            @return
            This function returns a valid report folder and annotation"""
    clean_log()
    if delta is not None and annot is None:
        return "delta(--d) should be in combination with annotation(--a)"
    if validate_input_paths(path_loc):
        return "Enter valid path"  # pragma: no mutate
    LOG.info("Input repository path validated successfully")  # pragma: no mutate
    if report_folder is None:
        report_folder = path_loc
    if validate_input_paths(report_folder):
        return "Enter valid report path"  # pragma: no mutate
    LOG.info("Input report folder path validated successfully")  # pragma: no mutate
    return report_folder, annot


# Generated: Function that initiates the overall process of extracting function/method definitions from the files
# Generated: Function that initiates the overall process of extracting function/method definitions from the files
# Generated: Function that initiates the overall process of extracting function/method definitions from the files
# Generated: Function that initiates the overall process of extracting function/method definitions from the files
def extractor(path_loc, annot=None, delta=None, functionstartwith=None, report_folder=None, exclude=None, ignoreDocumented=None,
              removeCppSignatures = None):
    """ Function that initiates the overall process of extracting function/method definitions from the files
        @parameters
        path_loc: directory path of the repository
        annot: given annotation condition (Ex: @staticmethod, @Test)
        delta: Required lines from method
        @return
        This function returns a data frame which contains the function/method names, body
        of the processed input files and line numbers
        @usage
        function_def_extractor(path to repo, "@test")
        the above function call initiates the process to run function definition extraction on
        all files with @test annotation of the repository given """
    start = time.time()
    if isinstance(initialize_values(delta, annot, path_loc, report_folder), str):  # pylint: disable=R1705
        return initialize_values(delta, annot, path_loc, report_folder)
    else:
        report_folder, annot = initialize_values(delta, annot, path_loc, report_folder)
    code_list = []
    line_nums = []
    for func_name in filter_files(filter_reg_files(get_file_names(path_loc), exclude)):
        LOG.info("Extracting %s", func_name)  # pragma: no mutate
        if delta is not None:
            get_delta_lines(func_name, annot, delta)
        else:
            functions, line_num = get_function_names(func_name, ignoreDocumented)
            if os.path.splitext(func_name)[1].upper() == ".PY":
                code_list, line_nums = process_py_files(code_list,line_nums, line_num, func_name, annot, functionstartwith)
            else:
                code_list, line_nums = process_input_files(line_num, line_nums, functions, annot, func_name, code_list, functionstartwith, removeCppSignatures)
    end = time.time()
    LOG.info("Extraction process took %s minutes", round((end - start) / 60, 3))  # pragma: no mutate
    LOG.info("%s vaild files has been analysed",  # pragma: no mutate
             len(filter_files(filter_reg_files(get_file_names(path_loc), exclude))))  # pragma: no mutate
    return (get_final_dataframe(delta, code_list, line_nums))
