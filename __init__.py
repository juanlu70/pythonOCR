# Allows us to reference other non test_...py and ..._test.py py files in our tests folder and from the parent folder. 
# Allows us to reference non .py files, like .json files
import sys
import os
    
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
    
sys.path.append(currentdir)
sys.path.append(parentdir)

