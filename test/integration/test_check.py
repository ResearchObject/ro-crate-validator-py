import pytest
import import_ipynb
import os
import sys
from pathlib import Path

# file = Path(os.path.abspath('')).resolve()
# parent, root = file.parent, file.parents[1]
# sys.path.append(os.path.join(str(root), "src"))
import src.semanticCheck as semanticCheck
import test.integration.module as module

testing_path = "test/samples/invalid"
extension = ""

# try:
#     import semanticCheck
# except ModuleNotFoundError:
#     print("nnno")

# try:
#     import teet
#     teet.q()
# except ModuleNotFoundError:
#     print("no")
# def __init__():
    

def test_descriptor():
    output = semanticCheck.self_descriptor_check(testing_path, extension)
    if len(output) == 2:
        assert output[1] == True
    else:
        assert output[2] == False

def test_direct_property():
    output = semanticCheck.direct_property_check(testing_path, extension)
    if len(output) == 2:
        assert output[1] == True
    else:
        assert output[2] == False

def test_referencing():
    output = semanticCheck.referencing_check(testing_path, extension)
    if len(output) == 2:
        assert output[1] == True
    else:
        assert output[2] == False

def test_encoding():
    output = semanticCheck.encoding_check(testing_path, extension)
    if len(output) == 2:
        assert output[1] == True
    else:
        assert output[2] == False

def test_workflow():
    output = semanticCheck.scripts_and_workflow_check(testing_path, extension)
    if len(output) == 2:
        output = output[1]
    else:
        output = output[2]
    
    assert isinstance(output, str) or isinstance(output, bool)

    
class TestClass:

    # def test_function_1(self):
    #     # Override the Python built-in input method 
    #     semanticCheck.input = referencing_check(testing_path, extension)
    #     # Call the function you would like to test (which uses input)
    #     output = semanticCheck.referencing_check(testing_path, extension)  
    #     assert output == 'aaa'

    def test_function_2(self):
        module.input = lambda: 'b1b'
        assert module.input == "1"
        output = module.function2()  
        assert output == 'bbb'       

    def teardown_method(self, method):
        # This method is being called after each test case, and it will revert input back to original function
        module.input = input





