## export all mxds within a folder to jpg files of the same name (resolution = 300 dpi)

import arcpy
import os
import sys

BIN_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,BIN_DIR)
import my_utilities_NFSEG as myut


# Set some reference values according to the ReferenceDefinitions class
#-------------------------------------------
MyDef = myut.ReferenceDefinitions()


# Set ArcGIS file format version
ARCFILEVERSION = MyDef.ArcCFileVersion

# DIR for the GIS Map Templates
TEMPLATEDIR = MyDef.GisTemplateDIR
#-------------------------------------------


print("Exporting jpeg maps related to Introductory Background Information Related(IBR): Active bnd, Grid Detail")


# xoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxox
#
# Setup PATHs and filenames
#
# xoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxox

# Get the working PATHs
cpath_py, cpath_py_upper, cpath_py_base = myut.get_current_PATHs()

print("current directory: " + str(cpath_py))
print("parent directory: " + str(cpath_py_upper))
print("grandparent directory: " + str(cpath_py_base))


# Check and Create sub-directories as needed
#-------------------------------------------

# Sub-directory called /figures
dir_figs = os.path.join(cpath_py, "figures")
if not os.path.exists(dir_figs):
    os.makedirs(dir_figs)
else:
    print('\nWARNING: subdirectory "figures" already exists - \n' +
          '\t existing files with the same name as those updated ' +
          'in this script will be overwritten!\n')
# END IF


# Sub-directory called /GIS
dir_GIS = os.path.join(cpath_py, "GIS")
if not os.path.exists(dir_GIS):
    os.makedirs(dir_GIS)
else:
    print('\nWARNING: subdirectory "GIS" already exists - \n' +
          '\t existing files with the same name as those updated ' +
          'in this script will be overwritten!\n')
# END IF
#-------------------------------------------
# ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo



# xoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxox
#
# Create Maps
#
# xoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxox

mxdnames = ['IBI_Map1_DepictionOfModelGrid.mxd',
            'IBI_Map2_NFSEG_Active_Model_Domain_and_GridExtent.mxd']

for mxdname in mxdnames:
    mxd = arcpy.mapping.MapDocument(TEMPLATEDIR + mxdname)
    arcpy.mapping.ExportToJPEG(mxd, (dir_figs + '/' + mxdname[:-3] + 'jpg'), resolution=300)
    print ("Processing " + mxdname)
    mxd.saveACopy(os.path.join(dir_GIS, mxdname), ARCFILEVERSION)

