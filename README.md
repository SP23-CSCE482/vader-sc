This is the repository for VADER-SC - A project to increase source code readability.    
     
First, create a virtual environment. Run ```python3 -m venv SC_Venv```   
Then, install the requirements. Run ```source SC_Venv/bin/activate && pip install -r requirements.txt```     
Finally, you should be good to run it. Run ```python3 FunctionDefSampler.py``` to automatically generate documentation using CodeT5 for every function in the Sample_Code directory - both Python and C++ files!    
     
If you don't have ctags installed (which is a system requirement to run the philips parser), run ```sudo apt-get install exuberant-ctags```