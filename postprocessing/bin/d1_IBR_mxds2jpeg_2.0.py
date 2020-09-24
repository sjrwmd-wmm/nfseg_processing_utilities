## export all mxds within a folder to jpg files of the same name (resolution = 300 dpi)

import arcpy
import os
import sys

BIN_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,BIN_DIR)
#PATH = (os.getcwd() + "\\" + "bin")
#sys.path.insert(0,PATH)

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


# Get the working PATHs
cpath_py, cpath_py_upper, cpath_py_base = myut.get_current_PATHs()

print("current directory: " + str(cpath_py))
print("parent directory: " + str(cpath_py_upper))
print("grandparent directory: " + str(cpath_py_base))


# Check and Create sub-directories as needed
#-------------------------------------------

# Sub-directory called /figures
dir_figs = (str(cpath_py) + "/figures")
if os.path.exists(dir_figs) == False:
    os.makedirs(dir_figs)
else:
    print('\nWARNING: subdirectory "figures" already exists - \n' +
          '\t existing files with the same name as those updated ' +
          'in this script will be overwritten!\n')
# END IF
#print("root directory for figures output: "+str(dir_XS))


# Sub-directory called /GIS
dir_GIS = (str(cpath_py) + "/GIS")
if os.path.exists(dir_GIS) == False:
    os.makedirs(dir_GIS)
else:
    print('\nWARNING: subdirectory "GIS" already exists - \n' +
          '\t existing files with the same name as those updated ' +
          'in this script will be overwritten!\n')
# END IF
#-------------------------------------------


mxdnames = ['IBI_Map1_DepictionOfModelGrid.mxd',
            'IBI_Map2_NFSEG_Active_Model_Domain_and_GridExtent.mxd']

for mxdname in mxdnames:
    mxd = arcpy.mapping.MapDocument(TEMPLATEDIR + mxdname)
    arcpy.mapping.ExportToJPEG(mxd, (dir_figs + '/' + mxdname[:-3] + 'jpg'), resolution=300)
    print ("Processing " + mxdname)
    mxd.saveACopy( (dir_GIS + '/' + mxdname), ARCFILEVERSION)

