## export all mxds within a folder to jpg files of the same name (resolution = 300 dpi)

import arcpy
import os

print("Exporting jpeg maps related to Calibration Results Parameters(CRP): Transmissivity, Leakance and Hydraulic Conductivity.")

###input derived from current location:
argfnl=sys.argv[1]
### check for more arguments in sysargv.  spaces in folder names!
arg_ct=-1
for arg in sys.argv:
    #print(arg)
    arg_ct=arg_ct+1
    if arg_ct>1:
        argfnl=argfnl+" "+arg
cpath_py='/'.join(argfnl.split('\\'))
up1=os.path.abspath(os.path.join(cpath_py, os.pardir))
cpath_py_upper='/'.join(up1.split('\\'))
up2=os.path.abspath(os.path.join(up1, os.pardir))
cpath_py_base='/'.join(up2.split('\\'))
##alternative for manual (debugging)
#cpath_py="T:/NFSEGv1_1/Workspace_PEST_case006e_UPD/pest_postproc"
#cpath_py_upper="T:/NFSEGv1_1/Workspace_PEST_case006e_UPD"
#cpath_py_base="T:/NFSEGv1_1"

print("current directory: "+str(cpath_py))
print("parent directory:" + str(cpath_py_upper))
print("grandparent directory:" + str(cpath_py_base))

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
    #arcpy.CreateFileGDB_management(cpath_py,simnam+"_ZB","9.3")
    print("geodatabase for this sim does not exist - stopping - run earlier scripts")
    exit()

gdbZB=cpath_py+"/"+simnam+"_ZB.gdb"
if arcpy.Exists(gdbZB):
    print("Zonebudget geodatabase for this sim exists - continuing ")
    #arcpy.Delete_management(gdb)#temp action for debugging
    #arcpy.CreateFileGDB_management(dir_sim_proc,simnam,"CURRENT")
    #exit()
else:
    #arcpy.CreateFileGDB_management(cpath_py,simnam+"_ZB","9.3")
    print("Zonebudget geodatabase for this sim does not exist - stopping - run earlier scripts")
    exit()







###MXDs

mxds = ["CRP_Map131_Modeled_DistributionHHC_FeetperDay_Model_L1.mxd",
        "CRP_Map132_Modeled_DistributionHHC_FeetperDay_Model_L3.mxd",
        "CRP_Map133_Modeled_DistributionHHC_FeetperDay_Model_L5.mxd",
        "CRP_Map134_Modeled_DistributionHHC_FeetperDay_Model_L7.mxd",
        "CRP_Map140_Modeled_DistributionLeakance_perDay_Model_L2.mxd",
        "CRP_Map141_Modeled_DistributionLeakance_perDay_Model_L4.mxd",
        "CRP_Map137_Modeled_DistributionVHC_FeetperDay_Model_L2.mxd",
        "CRP_Map138_Modeled_DistributionVHC_FeetperDay_Model_L4.mxd",
        "CRP_Map139_Modeled_DistributionVHC_FeetperDay_Model_L6.mxd",
        "CRP_Map135_Spatial_Distribution_of_T_with_Selected_APT_Results_Feet_Squared_perDay_Model_L3.mxd",
        "CRP_Map136_Spatial_Distribution_of_T_with_Selected_APT_Results_Feet_Squared_perDay_Model_L5.mxd"]

for mxdname in mxds:
    mxd = arcpy.mapping.MapDocument(cpath_py +'/templates/'+mxdname)
    lyrList = arcpy.mapping.ListLayers(mxd)
    for lyr in lyrList:
        if lyr.name[:5]=="Model" or lyr.name[:8]=="Leakance":
            print "updating layer "+lyr.name
            arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE","nfseg_props")
    print "updating "+mxdname
    arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
    mxd.saveACopy(cpath_py+'/'+mxdname,"9.0")


