#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
#   Collection of functions utilized within
#   multiple scripts within the NFSEG series.
#
#   Written: 20190719 PMBremner
#   Last Modified: 20190826 PMBremner
#
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

import sys
import os


# xoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxox
#
# A General Class to set global user defined values
# and reference values.
# 
#
# Last Modified: 20190826 PMBremner
#
# xoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxox
class ReferenceDefinitions:
    def __init__(self):
        
        # Set the PATH to the BIN directory where the scripts live
        self.BIN_DIR = os.path.dirname(os.path.realpath(__file__))
        
        
        # Set the PATH to the parent directory to the BIN_DIR
        self.SCRIPT_PARENT_DIR = '\\'.join(self.BIN_DIR.split('\\')[:-1])
        
        
        # Set the PATH to the GIS map templates from the SCRIPT_PARENT_DIR
        #self.GisTemplateDIR = ('C:/MODELS/TMP/PostProcessing_TestDIR/' +
        #                       'PostProcessing_Scripts_20190718/' +
        #                       'pest_postproc/templates/')
        self.GisTemplateDIR = (self.SCRIPT_PARENT_DIR + '\\templates\\')
        
        
        # Set the Arc GIS file format version number
        # NOTE: Choices are:
        #       ['8.3', '9.0', '9.2', '9.3', '10.0', '10.1', '10.3']
        self.ArcCFileVersion = '10.0' #'9.0'
        
# ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo



# xoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxox
#
# Capture and return the current working PATH,
# as well as the Parent and Grandparent directories.
#
# Input:  none required
#
# Output:
#   - the current working directory
#   - the parent directory
#   - the parent to the parent (grandparent) directory
#
# Last Modified: 20190722 PMBremner
#
# xoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxox
def get_current_PATHs():
    # Capture commandline input:
    #   - the full PATH of the current working directory
    #   - check for additional input caused by spaces in the PATH
    #   - split the input into the parent and base PATHs
    #
    #  !!!PMB!!!
    #       - Changed to simplfy the PATH capture -- 20190719
    #       - Old version commented out in case new version fails
    
    
    # Old Version:
    #argfnl=sys.argv[1]
    #### check for more arguments in sysargv.  spaces in folder names!
    #arg_ct=-1
    #for arg in sys.argv:
    #    #print(arg)
    #    arg_ct=arg_ct+1
    #    if arg_ct>1:
    #        argfnl=argfnl+" "+arg
    #cpath_py='/'.join(argfnl.split('\\'))
    #up1=os.path.abspath(os.path.join(cpath_py, os.pardir))
    #cpath_py_upper='/'.join(up1.split('\\'))
    #up2=os.path.abspath(os.path.join(up1, os.pardir))
    #cpath_py_base='/'.join(up2.split('\\'))
    ###alternative for manual (debugging)
    ##cpath_py="T:/NFSEGv1_1/Workspace_PEST_case006e_UPD/pest_postproc"
    ##cpath_py_upper="T:/NFSEGv1_1/Workspace_PEST_case006e_UPD"
    ##cpath_py_base="T:/NFSEGv1_1"
    #
    # New Version:
    CurWorkingDir='/'.join(os.getcwd().split('\\'))
    ParentDir='/'.join(os.getcwd().split('\\')[:-1])
    GrandparentDir='/'.join(os.getcwd().split('\\')[:-2])
    
    return CurWorkingDir, ParentDir, GrandparentDir
# ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo



# xoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxox
#
# Find a unique filename in a directory (SEARCHDIR) based
# only on the file suffix. If found, return the file basename.
#
# NOTE: This function can only be used to search for a file whose suffix
#       is unique among all other files in SEARCHDIR.
#
# Example:
#   SEARCHDIR contains many files, but only one whose filename ends
#   in the suffix ".res". This function can be used to find this file.
#
#   SEARCHDIR contains many files that end in the suffix ".txt". This
#   function CANNOT be used to find a unique ".txt" file in this
#   SEARCHDIR because there are multiple instances of ".txt".
#
# This function checks that only one of these files exist.
# An exception (error) is thrown otherwise, and the program stops.
#
# 
# Input:
#   - searchdir = the directory to search in
#   - suffix = the suffix to search for
#              NOTE: It does not matter if the suffix
#                    includes a period at the beginning. A
#                    period will be inserted if it is missing.
#
# Output:
#   - foundfile = the base of the simulation filename
#
#
# Last Modified: 20190722 PMBremner
#
# xoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxox
def get_unique_filebasename_from_suffix(searchdir, suffix):
    
    # Add the period before the suffix if it
    # is not already there.
    # Set the total length of the suffix plus period
    if (suffix[0]=='.'):
        numchar = len(suffix)
    else:
        suffix = ('.' + suffix)
        numchar = len(suffix)
    
    # Initialize the number of found files
    num_foundfiles=0
    
    # March through all the files and count number of
    # times the desired suffix is encountered
    for file in os.listdir(searchdir):
        if str(file[-numchar:])==suffix:
            foundfile=file[:-numchar]
            num_foundfiles=num_foundfiles+1
    #  END for loop over file
    
    # Check if a unique file was found
    if num_foundfiles==0:
        raise Exception('I am deeply sorry, but no files were found with the suffix: {}'.format(suffix))
    elif num_foundfiles>1:
        raise Exception("Don't know what to do! Multiple files were found with the suffix: {}".format(suffix))
    # END if
#    else:
#        print("sim name:"+str(foundfile))
    
    return foundfile
# ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo



# xoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxox
#
# Determine whether the input value is a number, or other type.
#
# 
# Input:
#   - s = value to be checked
#
# Output:
#   - boolean True (value is a number) or False (not a number)
#
#
# Last Modified: 20190724 PMBremner
#
# xoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxox
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
# ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo



