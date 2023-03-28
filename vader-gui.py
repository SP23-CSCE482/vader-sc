import PySimpleGUI as sg
import subprocess as sp
import sys

sg.theme('DarkBlack 1')   # Add a touch of color
# All the stuff inside your window.

# This function does the actual "running" of the command.  Also watches for any output. If found output is printed
def runCommand(cmd, timeout=None, window=None):
    p = sp.Popen(cmd, shell=True, stdout=sp.PIPE, stderr=sp.STDOUT)
    output = ''
    for line in p.stdout:
        line = line.decode(errors='replace' if (sys.version_info) < (3, 5) else 'backslashreplace').rstrip()
        output += line
        print(line)
        window.Refresh() if window else None        # yes, a 1-line if, so shoot me
    retval = p.wait(timeout)
    return (retval, output)                         # also return the output just for fun

flags = [sg.Checkbox("ignore-documented", key="ignore-documented", default=False, tooltip="ignores documented functions"),
            sg.Checkbox("remove-cpp-signatures", key="remove-cpp-signatures", default=False, tooltip="removes signatures of C++ functions before processing"),
            sg.Checkbox("overwrite-files", key="overwrite-files", default=False, tooltip="overwrites original files with generated comments instead of creating new ones"),
            sg.Checkbox("non-recursive", key="non-recursive", default=False, tooltip="only generate comments for files in immediate directory and not children directories"),
            sg.Checkbox("verbose", key="verbose", default=False, tooltip="display verbose output during program execution"),
            sg.Checkbox("cuda", key="cuda", default=False, tooltip="uses NVIDIA GPU for inference. Make sure appropriate drivers/libraries are installed."),
            sg.Checkbox("new-directories", key="new-directories", default=False, tooltip="creates new directories within which to put code with generated comments")
            ]
layout = [ [sg.Text('Directory of Source Code:'), sg.Input(key='-USER FOLDER-'), sg.FolderBrowse(target='-USER FOLDER-')],
           flags,
           [sg.Button('Generate Comments', key = "GC")],
           [sg.Output(size=(100,20))] ]

# Create the Window
window = sg.Window('VADER-SC GUI', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    if event == 'GC':
        #directly fetching this is weird but it works
        path = layout[0][1].get()
        if(len(path) == 0):
            sg.Popup('Directory Path cannot be empty')
        else:
            command = ["python3","vader.py",path]
            for flag in flags:
                if(flag.get()):
                    command.append("--" + flag.key)
                    print("using flag", flag.key)
            runCommand(" ".join(command),window = window)



window.close()