### export all mxds within a folder to jpg files of the same name (resolution = 300 dpi)

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


print("Exporting jpeg maps related to Calibration Parameter Related(CPR): Horizontal Heads, Vertical Heads and Head Multipliers for L2, L3 and L5.")


# Get the working PATHs
cpath_py, cpath_py_upper, cpath_py_base = myut.get_current_PATHs()

print("current directory: " + str(cpath_py))
print("parent directory: " + str(cpath_py_upper))
print("grandparent directory: " + str(cpath_py_base))


###check for a sub directory called /figures, create it if necessary
dir_figs=str(cpath_py)+"/figures"
if os.path.exists(dir_figs) == False:
    os.makedirs(dir_figs)
else:
    print("subdirectory / figures directory already exists - existing files will get overwritten without any further warning")
#print("root directory for figures output: "+str(dir_XS))

#find optimal parameters output file (*.pst.txt) - the rest of the files get named with the pst file name in it
num_simnams=0
for file in os.listdir(cpath_py_upper):
    if str(file[-4:])=='.pst':
        simnam=file[:-4]
        num_simnams=num_simnams+1
if num_simnams==0:
    print("looked for a *.pst file - but found none - stopping")
    exit()
elif num_simnams>1:
    print("multiple *.pst files found in this folder - stopping")
    exit()
else:
    print("sim name:"+str(simnam))

gdb=cpath_py+"/"+simnam+".gdb"
if arcpy.Exists(gdb):
    print("geodatabase for this sim exists - continuing ")
    #arcpy.Delete_management(gdb)#temp action for debugging
    #arcpy.CreateFileGDB_management(dir_sim_proc,simnam,"CURRENT")
    #exit()
else:
    #arcpy.CreateFileGDB_management(cpath_py,simnam+"_ZB", ARCFILEVERSION)
    print("geodatabase for this sim does not exist - stopping - run earlier scripts")
    exit()


###MXDs
mxdname = 'CPR_Map69_DistributionHHC_PP_Model_L1.mxd'
mxd = arcpy.mapping.MapDocument(TEMPLATEDIR + mxdname)
lyrList = arcpy.mapping.ListLayers(mxd)
for lyr in lyrList:
    if lyr.name[:13]=="Model Layer 1":
        print lyr.name
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",simnam+"_ppkx1_feet")
print "updating "+mxdname
arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
mxd.saveACopy(cpath_py+'/'+mxdname, ARCFILEVERSION)

mxdname = 'CPR_Map70_DistributionHHC_PP_Model_L3.mxd'
mxd = arcpy.mapping.MapDocument(TEMPLATEDIR + mxdname)
lyrList = arcpy.mapping.ListLayers(mxd)
for lyr in lyrList:
    if lyr.name[:13]=="Model Layer 3":
        print lyr.name
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",simnam+"_ppkx3_feet")
print "updating "+mxdname
arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
mxd.saveACopy(cpath_py+'/'+mxdname, ARCFILEVERSION)

mxdname = 'CPR_Map71_DistributionHHC_PP_Model_L7.mxd'
mxd = arcpy.mapping.MapDocument(TEMPLATEDIR + mxdname)
lyrList = arcpy.mapping.ListLayers(mxd)
for lyr in lyrList:
    if lyr.name[:13]=="Model Layer 7":
        print lyr.name
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",simnam+"_ppkx7_feet")
print "updating "+mxdname
arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
mxd.saveACopy(cpath_py+'/'+mxdname, ARCFILEVERSION)

mxdname = 'CPR_Map72_DistributionVHC_PP_Model_L6.mxd'
mxd = arcpy.mapping.MapDocument(TEMPLATEDIR + mxdname)
lyrList = arcpy.mapping.ListLayers(mxd)
for lyr in lyrList:
    if lyr.name[:13]=="Model Layer 6":
        print lyr.name
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",simnam+"_ppkz6_feet")
print "updating "+mxdname
arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
mxd.saveACopy(cpath_py+'/'+mxdname, ARCFILEVERSION)

mxdname = 'CPR_Map73_DistributionVHC_PP_and_VHC_PP_and_VHC_Multiplier_PP_Model_L2.mxd'
mxd = arcpy.mapping.MapDocument(TEMPLATEDIR + mxdname)
lyrList = arcpy.mapping.ListLayers(mxd)
for lyr in lyrList:
    if lyr.name[:13]=="Model Layer 2":
        print lyr.name
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",simnam+"_ppkz2_feet")
print "updating "+mxdname
arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
mxd.saveACopy(cpath_py+'/'+mxdname, ARCFILEVERSION)

mxdname = 'CPR_Map74_DistributionVHC_PP_and_VHC_PP_and_VHC_Multiplier_PP_Model_L4.mxd'
mxd = arcpy.mapping.MapDocument(TEMPLATEDIR + mxdname)
lyrList = arcpy.mapping.ListLayers(mxd)
for lyr in lyrList:
    if lyr.name[:13]=="Model Layer 4":
        print lyr.name
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",simnam+"_ppkz4_feet")
print "updating "+mxdname
arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
mxd.saveACopy(cpath_py+'/'+mxdname, ARCFILEVERSION)

mxdname = "CPR_Map75_DistributionVHC_PP_and_VHC_Multiplier_PP_Model_L5.mxd"
mxd = arcpy.mapping.MapDocument(TEMPLATEDIR + mxdname)
lyrList = arcpy.mapping.ListLayers(mxd)
for lyr in lyrList:
    if lyr.name[:13]=="Model Layer 5":
        print lyr.name
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",simnam+"_ppkx5_feet")
print "updating "+mxdname
arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
mxd.saveACopy(cpath_py+'/'+mxdname, ARCFILEVERSION)
