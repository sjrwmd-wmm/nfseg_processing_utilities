"""
A script just to test various PATH related things.

Started 20190827. PMBremner
"""


# Test the capturing the working directory
# and script directory
import os
import sys


#print (os.path.dirname(os.path.realpath(__file__)))

#print (os.path.dirname(os.path.realpath(sys.path[0])))

BIN_DIR = os.path.dirname(os.path.realpath(__file__))

#PATH = (BIN_DIR)
sys.path.insert(0,BIN_DIR)

import my_utilities_NFSEG as myut

SCRIPT_PARENT_DIR = '\\'.join(BIN_DIR.split('\\')[:-1])
TEMPLATESDIR = (SCRIPT_PARENT_DIR + '\\templates\\')

print (BIN_DIR)
print (SCRIPT_PARENT_DIR)
print (TEMPLATESDIR)


# Set some reference values according to the ReferenceDefinitions class
#-------------------------------------------
MyDef = myut.ReferenceDefinitions()


# Set ArcGIS file format version
ARCFILEVERSION = MyDef.ArcCFileVersion

# DIR for the GIS Map Templates
TEMPLATEDIR_REF = MyDef.GisTemplateDIR
BIN_DIR_REF = MyDef.BIN_DIR
SCRIPT_PARENT_DIR_REF = MyDef.SCRIPT_PARENT_DIR
#-------------------------------------------


print (BIN_DIR_REF)
print (SCRIPT_PARENT_DIR_REF)
print (TEMPLATEDIR_REF)
print (ARCFILEVERSION)

