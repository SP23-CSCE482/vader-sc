# Vader-SC
This is the repository for VADER-SC - A project to increase source code readability. 

## Usage
* To parse directory run ```python3 vader.py /path/to/directory```

* To use GUI cd into vader-sc/ and run ```./vader-gui.sh``` or run ```source SC_Venv/bin/activate && python3 vader-gui.py```

* If using WSL, performance will be very slow to analyze mounted folders (/mnt/c/)
* Consider moving folders into WSL, then generating comments within WSL

## Installation Script

* To install using the script you must be root and you must run ```chmod +x install.sh && sudo ./install.sh``` inside the folder.
* You must download the model so the program runs properly (~800+ MB).
* You can add alias to the program by running ```alias vader-sc='$PWD/SC_Venv/bin/python3 $PWD/vader.py'``` so it can be used anywhere
* if you have any issues with the installtion script please do a manual installation.


## Local Setup 
* If you don't have ctags installed (which is a system requirement to run the philips parser), run ```sudo apt-get install exuberant-ctags```

* To run the gui, you need to install python3-tk as well
* Run ```sudo apt-get install python3-tk```

* cd into the directory vader-sc 

* create a virtual environment, and install the requirements. 
  * Run ```python3 -m venv SC_Venv && source SC_Venv/bin/activate && python -m pip install --upgrade pip && pip install -r requirements.txt -vvv```     
