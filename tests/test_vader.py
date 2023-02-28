import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from vader import parse_df_to_dict
import pytest
import pandas as pd

def test_parse_df_to_dict():
    initial_dict = {
        "Uniq ID": ["Sample_Code/Camera.cpp_Camera","Sample_Code/FastFourierTransforms.py_FastFourierTransform","Sample_Code/threadSafeQueue.cpp_isEmpty"],
        "Code": ["print(\"Hello World!\")","print(\"Goodbye World!\")", "print(\"World?\")"],
        "Line": ["Sample_Code/Camera","Sample_Code/FastFourierTransforms","Sample_Code/threadSafeQueue"]
    }
    test_df = pd.DataFrame(initial_dict)

    transformed_dict = parse_df_to_dict(test_df)

    assert set(["Sample_Code/Camera.cpp","Sample_Code/FastFourierTransforms.py","Sample_Code/threadSafeQueue.cpp"]) == set(transformed_dict.keys())
    