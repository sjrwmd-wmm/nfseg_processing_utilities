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


print("Exporting jpeg maps related to Calibration_Results_Flows(CRF): Spring Flows, 1st Mag Springs, Baseflow Pickups, Net Recharge and Upward/Downward Flows L2 L4.")


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

gdbZB=cpath_py+"/"+simnam+"_ZB.gdb"
if arcpy.Exists(gdbZB):
    print("Zonebudget geodatabase for this sim exists - continuing ")
    #arcpy.Delete_management(gdb)#temp action for debugging
    #arcpy.CreateFileGDB_management(dir_sim_proc,simnam,"CURRENT")
    #exit()
else:
    #arcpy.CreateFileGDB_management(cpath_py,simnam+"_ZB", ARCFILEVERSION)
    print("Zonebudget geodatabase for this sim does not exist - stopping - run earlier scripts")
    exit()


###MXDs
mxdname = 'CRF_Map109_Magnitude1Springs_EstimatedFlowrates_and_FlowrateResiduals_cfs_2001.mxd'
mxd = arcpy.mapping.MapDocument(TEMPLATEDIR + mxdname)
lyrList = arcpy.mapping.ListLayers(mxd)
for lyr in lyrList:
    if lyr.name[:6]=="Spring":
        print ("updating layer " + lyr.name)
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",simnam+"_qsprings_1st_2001")
print ("updating " + mxdname)
arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
mxd.saveACopy(cpath_py+'/'+mxdname, ARCFILEVERSION)

mxdname = 'CRF_Map110_Magnitude1Springs_EstimatedFlowrates_and_FlowrateResiduals_cfs_2009.mxd'
mxd = arcpy.mapping.MapDocument(TEMPLATEDIR + mxdname)
lyrList = arcpy.mapping.ListLayers(mxd)
for lyr in lyrList:
    if lyr.name[:6]=="Spring":
        print ("updating layer " + lyr.name)
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",simnam+"_qsprings_1st_2009")
print ("updating " + mxdname)
arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
mxd.saveACopy(cpath_py+'/'+mxdname, ARCFILEVERSION)

mxds_qr = ["CRF_Map115_EstimatedBaseflowPickup_Residuals_cfs_Region_C_2001.mxd",
             "CRF_Map113_EstimatedBaseflowPickup_Residuals_cfs_Region_A_2001.mxd",
             "CRF_Map114_EstimatedBaseflowPickup_Residuals_cfs_Region_B_2001.mxd",
             "CRF_Map119_EstimatedBaseflowPickup_Residuals_cfs_Region_C_2009.mxd",
             "CRF_Map117_EstimatedBaseflowPickup_Residuals_cfs_Region_A_2009.mxd",
             "CRF_Map118_EstimatedBaseflowPickup_Residuals_cfs_Region_B_2009.mxd"]
for mxdname in mxds_qr:
    mxd = arcpy.mapping.MapDocument(TEMPLATEDIR + mxdname)
    lyrList = arcpy.mapping.ListLayers(mxd)
    for lyr in lyrList:
        if lyr.name[:4]=="Gage":
            print ("updating layer " + lyr.name)
            arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",simnam+"_qr_20012009")
    print ("updating " + mxdname)
    arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
    mxd.saveACopy(cpath_py+'/'+mxdname, ARCFILEVERSION)

mxds_qs = ["CRF_Map120_EstimatedCumulative_BaseflowResiduals_cfs_2009.mxd",
           "CRF_Map116_EstimatedCumulative_BaseflowResiduals_cfs_2001.mxd"]
for mxdname in mxds_qs :
    mxd = arcpy.mapping.MapDocument(TEMPLATEDIR + mxdname)
    lyrList = arcpy.mapping.ListLayers(mxd)
    for lyr in lyrList:
        if lyr.name[:4]=="Gage":
            print ("updating " + lyr.name)
            arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",simnam+"_qs_20012009")
        if lyr.name[:12]=="Contributing":
            print ("updating " + lyr.name)
            arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",simnam+"_qrqs_gagepoly_NCB")
    arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
    print ("updated " + mxdname)
    mxd.saveACopy(cpath_py+'/'+mxdname, ARCFILEVERSION)

mxds_netrch = ["CRF_Map121_Simulated_Net_Recharge_Rates_ipy_2001.mxd",
               "CRF_Map122_Simulated_Net_Recharge_Rates_ipy_2009.mxd"]
for mxdname in mxds_netrch:
    yy = mxdname[-6:-4]
    mxd = arcpy.mapping.MapDocument(TEMPLATEDIR + mxdname)
    lyrList = arcpy.mapping.ListLayers(mxd)
    for lyr in lyrList:
        if lyr.name[:17]=="NFSEG_NetRecharge":
            print ("updating layer " + lyr.name)
            arcpy.mapping.Layer.replaceDataSource(lyr,gdbZB,"FILEGDB_WORKSPACE","cbb_props_calcs"+str(yy))
    print ("updating " + mxdname)
    arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
    mxd.saveACopy(cpath_py+'/'+mxdname, ARCFILEVERSION)

mxds_L2Qz = ["CRF_Map123b_FlowThrough_LowerFace_L2_2001_ULR_L3to2_ipy.mxd",
             "CRF_Map123a_FlowThrough_LowerFace_L2_2001_DLR_L2to3_ipy.mxd",
             "CRF_Map124b_FlowThrough_LowerFace_L2_2009_ULR_L3to2_ipy.mxd",
             "CRF_Map124a_FlowThrough_LowerFace_L2_2009_DLR_L2to3_ipy.mxd"]
for mxdname in mxds_L2Qz:
    yy = mxdname[-20:-18]
    mxd = arcpy.mapping.MapDocument(TEMPLATEDIR + mxdname)
    lyrList = arcpy.mapping.ListLayers(mxd)
    for lyr in lyrList:
        if lyr.name[:7]=="Leakage":
            print ("updating layer " + lyr.name)
            arcpy.mapping.Layer.replaceDataSource(lyr,gdbZB,"FILEGDB_WORKSPACE","cbb_props_calcs"+str(yy))
    print ("updating " + mxdname)
    arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
    mxd.saveACopy(cpath_py+'/'+mxdname, ARCFILEVERSION)

mxds_L4Qz = ["CRF_Map125a_FlowThrough_LowerFace_L4_2001_DLR_L4to5_ipy.mxd",
             "CRF_Map125b_FlowThrough_LowerFace_L4_2001_ULR_L5to4_ipy.mxd",
             "CRF_Map126a_FlowThrough_LowerFace_L4_2009_DLR_L4to5_ipy.mxd",
             "CRF_Map126b_FlowThrough_LowerFace_L4_2009_ULR_L5to4_ipy.mxd"]
for mxdname in mxds_L4Qz:
    yy = mxdname[-20:-18]
    mxd = arcpy.mapping.MapDocument(TEMPLATEDIR + mxdname)
    lyrList = arcpy.mapping.ListLayers(mxd)
    for lyr in lyrList:
        if lyr.name[:7]=="Leakage":
            print ("updating layer " + lyr.name)
            arcpy.mapping.Layer.replaceDataSource(lyr,gdbZB,"FILEGDB_WORKSPACE","cbb_props_calcs"+str(yy))
    print ("updating " + mxdname)
    arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
    mxd.saveACopy(cpath_py+'/'+mxdname, ARCFILEVERSION)