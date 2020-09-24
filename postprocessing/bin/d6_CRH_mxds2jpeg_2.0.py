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


print("Exporting jpeg maps related to Calibration Results Heads(CRH): Contour POT maps, Residual Heads and Water Table above Land Surface.")


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
#group - non-updated mxds (100% from template gdb)
mxds_noupd = ['CRH_Map76_EstimatedPOT_UFA_2001_Based_on_2001_UFA_Observation_Data.mxd',
              'CRH_Map77_EstimatedPOT_UFA_2009_Based_on_2009_UFA_Observation_Data.mxd']
for mxdname in mxds_noupd:
    mxd = arcpy.mapping.MapDocument(TEMPLATEDIR + mxdname)
    print ("reprinting " + mxdname)
    arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)

#individually-updated mxds
mxdname = 'CRH_Map78_Simulated_POT_SurfaceModel_L3_2001.mxd'
mxd = arcpy.mapping.MapDocument(TEMPLATEDIR + mxdname)
lyrList = arcpy.mapping.ListLayers(mxd)
for lyr in lyrList:
    if lyr.name=="Sim Pot Surface L3 -Index Contour (50ft)":
        print ("updating layer:" + lyr.name)
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE","ref_HDS_L03SP1TS1_cont50ft")
    elif lyr.name=="Sim Pot Surface L3 - Contour 5 ft Interval":
        print "updating layer:"+lyr.name
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE","ref_HDS_L03SP1TS1_cont5ft")
print "updating "+mxdname
arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
mxd.saveACopy(cpath_py+'/'+mxdname, ARCFILEVERSION)

mxdname = 'CRH_Map79_Simulated_POT_SurfaceModel_L3_2009.mxd'
mxd = arcpy.mapping.MapDocument(TEMPLATEDIR + mxdname)
lyrList = arcpy.mapping.ListLayers(mxd)
for lyr in lyrList:
    if lyr.name=="Sim Pot Surface L3 -Index Contour (50ft)":
        print "updating layer:"+lyr.name
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE","ref_HDS_L03SP2TS1_cont50ft")
    elif lyr.name=="Sim Pot Surface L3 - Contour 5 ft Interval":
        print "updating layer:"+lyr.name
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE","ref_HDS_L03SP2TS1_cont5ft")
print "updating "+mxdname
arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
mxd.saveACopy(cpath_py+'/'+mxdname, ARCFILEVERSION)

mxdname = "CRH_Map80_Simulated_WT_L1_2001.mxd"
mxd = arcpy.mapping.MapDocument(TEMPLATEDIR + mxdname)
lyrList = arcpy.mapping.ListLayers(mxd)
for lyr in lyrList:
    if lyr.name=="Sim Water Surface L1 -Index Contour (50ft)":
        print "updating layer:"+lyr.name
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE","ref_HDS_L01SP1TS1_cont50ft")
    elif lyr.name=="Sim Water Surface L1 - Contour 5 ft Interval":
        print "updating layer:"+lyr.name
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE","ref_HDS_L01SP1TS1_cont5ft")
print "updating "+mxdname
arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
mxd.saveACopy(cpath_py+'/'+mxdname, ARCFILEVERSION)

mxdname = "CRH_Map81_Simulated_WT_L1_2009.mxd"
mxd = arcpy.mapping.MapDocument(TEMPLATEDIR + mxdname)
lyrList = arcpy.mapping.ListLayers(mxd)
for lyr in lyrList:
    if lyr.name=="Sim Water Surface L1 -Index Contour (50ft)":
        print "updating layer:"+lyr.name
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE","ref_HDS_L01SP2TS1_cont50ft")
    elif lyr.name=="Sim Water Surface L1 - Contour 5 ft Interval":
        print "updating layer:"+lyr.name
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE","ref_HDS_L01SP2TS1_cont5ft")
print "updating "+mxdname
arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
mxd.saveACopy(cpath_py+'/'+mxdname, ARCFILEVERSION)

mxdname = "CRH_Map82_Simulated_POT_Surface_Model_L5_2001.mxd"
mxd = arcpy.mapping.MapDocument(TEMPLATEDIR + mxdname)
lyrList = arcpy.mapping.ListLayers(mxd)
for lyr in lyrList:
    if lyr.name=="Sim Water Surface L5 -Index Contour (50ft)":
        print "updating layer:"+lyr.name
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE","ref_HDS_L05SP1TS1_cont50ft")
    elif lyr.name=="Sim Water Surface L5 - Contour 5 ft Interval":
        print "updating layer:"+lyr.name
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE","ref_HDS_L05SP1TS1_cont5ft")
print "updating "+mxdname
arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
mxd.saveACopy(cpath_py+'/'+mxdname, ARCFILEVERSION)

mxdname = "CRH_Map83_Simulated_POT_Surface_Model_L5_2009.mxd"
mxd = arcpy.mapping.MapDocument(TEMPLATEDIR + mxdname)
lyrList = arcpy.mapping.ListLayers(mxd)
for lyr in lyrList:
    if lyr.name=="Sim Water Surface L5 -Index Contour (50ft)":
        print "updating layer:"+lyr.name
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE","ref_HDS_L05SP2TS1_cont50ft")
    elif lyr.name=="Sim Water Surface L5 - Contour 5 ft Interval":
        print "updating layer:"+lyr.name
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE","ref_HDS_L05SP2TS1_cont5ft")
print "updating "+mxdname
arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
mxd.saveACopy(cpath_py+'/'+mxdname, ARCFILEVERSION)

mxds_HH = ["CRH_Map84_ResidualsHH_Feet_Model_L1_2001.mxd",
          "CRH_Map89_ResidualsHH_Feet_Model_L5_2009.mxd",
          "CRH_Map88_ResidualsHH_Feet_Model_L5_2001.mxd",
          "CRH_Map87_ResidualsHH_Feet_Model_L3_2009.mxd",
          "CRH_Map86_ResidualsHH_Feet_Model_L3_2001.mxd",
          "CRH_Map85_ResidualsHH_Feet_Model_L1_2009.mxd"]
for mxdname in mxds_HH:
    mxd = arcpy.mapping.MapDocument(TEMPLATEDIR + mxdname)
    yy = mxdname[-6:-4]
    lyrList = arcpy.mapping.ListLayers(mxd)
    for lyr in lyrList:
        if lyr.name[:5]=="Water":
            print "updating layer:"+lyr.name
            arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",simnam+"_WL_targets_20"+str(yy))
    print "updating "+mxdname
    arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
    mxd.saveACopy(cpath_py+'/'+mxdname, ARCFILEVERSION)
    #mxd.save()

mxds_VHD_L1L3 = ["CRH_Map97_ResidualsVHD_Feet_Model_Layers_1_and_3_2001.mxd",
             "CRH_Map98_ResidualsVHD_Feet_Model_Layers_1_and_3_2009.mxd",]
for mxdname in mxds_VHD_L1L3:
    mxd = arcpy.mapping.MapDocument(TEMPLATEDIR + mxdname)
    yy = mxdname[-6:-4]
    lyrList = arcpy.mapping.ListLayers(mxd)
    for lyr in lyrList:
        if lyr.name[:3]=="VHD":
            print "updating layer:"+lyr.name
            arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",simnam+"_VHD_L1L3_targets_20"+str(yy))
        elif lyr.name[:8]=="Residual":
            print "updating layer:"+lyr.name
            arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",simnam+"_VHD_L1L3_targets_20"+str(yy))
    print "updating "+mxdname
    arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
    mxd.saveACopy(cpath_py+'/'+mxdname, ARCFILEVERSION)
    #mxd.save()

mxds_VHD_L3L5 = ["CRH_Map100_ResidualsVHD_Feet_Model_Layers_3_and_5_2009.mxd",
             "CRH_Map99_ResidualsVHD_Feet_Model_Layers_3_and_5_2001.mxd"]
for mxdname in mxds_VHD_L3L5:
    mxd = arcpy.mapping.MapDocument(TEMPLATEDIR + mxdname)
    yy = mxdname[-6:-4]
    lyrList = arcpy.mapping.ListLayers(mxd)
    for lyr in lyrList:
        if lyr.name[:3]=="VHD":
            print "updating layer:"+lyr.name
            arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",simnam+"_VHD_L3L5_targets_20"+str(yy))
        elif lyr.name[:8]=="Residual":
            print "updating layer:"+lyr.name
            arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",simnam+"_VHD_L3L5_targets_20"+str(yy))
    print "updating "+mxdname
    arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
    mxd.saveACopy(cpath_py+'/'+mxdname, ARCFILEVERSION)
    #mxd.save()

mxds_HHDs = ["CRH_Map106_ResidualsHHD_Feet_Model_L3_2009.mxd",
             "CRH_Map105_ResidualsHHD_Feet_Model_L3_2001.mxd"]
for mxdname in mxds_HHDs:
    mxd = arcpy.mapping.MapDocument(TEMPLATEDIR + mxdname)
    yy = mxdname[-6:-4]
    lyrList = arcpy.mapping.ListLayers(mxd)
    for lyr in lyrList:
        if lyr.name[:3]=="HHD":
            print "updating layer:"+lyr.name
            arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",simnam+"_HHD_L3_targets_"+str(yy))
        elif lyr.name[:8]=="Residual":
            print "updating layer:"+lyr.name
            arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",simnam+"_HHD_L3_targets_"+str(yy))
    print "updating "+mxdname
    arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
    mxd.saveACopy(cpath_py+'/'+mxdname, ARCFILEVERSION)
    #mxd.save()

mxds_fld = ["CRH_Map144_HeightSimWT_above_LS_FT_2001.mxd",
            "CRH_Map145_HeightSimWT_above_LS_FT_2009.mxd",
            "CRH_Map146_Difference_HeightSim_WT_above_LS_FT_Pumps-Off_to2009.mxd"]
for mxdname in mxds_fld:
    mxd = arcpy.mapping.MapDocument(TEMPLATEDIR + mxdname)
    lyrList = arcpy.mapping.ListLayers(mxd)
    for lyr in lyrList:
        if lyr.name[:6]=="Height":
            print "updating layer:"+lyr.name
            arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE","nfseg_props")
        elif lyr.name[:10]=="Difference": 
            print "updating layer:"+lyr.name
            arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE","nfseg_props_PUMPSOFF")
    print "updating "+mxdname
    arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
    mxd.saveACopy(cpath_py+'/'+mxdname, ARCFILEVERSION)
    #mxd.save()
