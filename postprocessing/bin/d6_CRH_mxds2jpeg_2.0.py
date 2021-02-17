## export all mxds within a folder to jpg files of the same name (resolution = 300 dpi)
#
# Create CRH maps 76-146

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


print("Exporting jpeg maps related to Calibration Results Heads(CRH): Contour POT maps, Residual Heads and Water Table above Land Surface.")


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

# Find PEST optimal parameters output file (*.pst) in the parent directory
# and get the basename to attach to output files generated by this script
simnam = myut.get_unique_filebasename_from_suffix(cpath_py_upper,'.pst')
print("sim name: {}".format(simnam))


gdb = os.path.join(cpath_py, simnam+".gdb")
if arcpy.Exists(gdb):
    print('geodatabase for this sim exists - continuing\n')
    #arcpy.Delete_management(gdb)#temp action for debugging
    #arcpy.CreateFileGDB_management(dir_sim_proc,simnam,"CURRENT")
    #exit()
else:
    #arcpy.CreateFileGDB_management(cpath_py,simnam+"_ZB", ARCFILEVERSION)
    errmsg = 'ERROR: geodatabase for this sim does not exist - stopping - run earlier scripts'
    raise Exception(errmsg)
# ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo



# xoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxox
#
# Create Maps
#
# xoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxoxox

# Group - non-updated maps (100% from template gdb)
map_noupd = ['CRH_Map76_EstimatedPOT_UFA_2001_Based_on_2001_UFA_Observation_Data',
              'CRH_Map77_EstimatedPOT_UFA_2009_Based_on_2009_UFA_Observation_Data']
for mapname in map_noupd:
    mxd = arcpy.mapping.MapDocument(TEMPLATEDIR + mapname + '.mxd')
    print ("reprinting {}.mxd".format(mapname))
    arcpy.mapping.ExportToJPEG(mxd, os.path.join(dir_figs, (mapname+'.jpg')), resolution=300)


# Groups of updated mmaps
properties = [
        ['CRH_Map78_Simulated_POT_SurfaceModel_L3_2001',
         ["Sim Pot Surface L3 -Index Contour (50ft)", "ref_HDS_L03SP1TS1_cont50ft"],
         ["Sim Pot Surface L3 - Contour 5 ft Interval", "ref_HDS_L03SP1TS1_cont5ft"]],
        ['CRH_Map79_Simulated_POT_SurfaceModel_L3_2009',
         ["Sim Pot Surface L3 -Index Contour (50ft)", "ref_HDS_L03SP2TS1_cont50ft"],
         ["Sim Pot Surface L3 - Contour 5 ft Interval", "ref_HDS_L03SP2TS1_cont5ft"]],
        ['CRH_Map80_Simulated_WT_L1_2001',
         ["Sim Water Surface L1 -Index Contour (50ft)", "ref_HDS_L01SP1TS1_cont50ft"],
         ["Sim Water Surface L1 - Contour 5 ft Interval", "ref_HDS_L01SP1TS1_cont5ft"]],
        ['CRH_Map81_Simulated_WT_L1_2009',
         ["Sim Water Surface L1 -Index Contour (50ft)", "ref_HDS_L01SP2TS1_cont50ft"],
         ["Sim Water Surface L1 - Contour 5 ft Interval", "ref_HDS_L01SP2TS1_cont5ft"]],
        ['CRH_Map82_Simulated_POT_Surface_Model_L5_2001',
         ["Sim Water Surface L5 -Index Contour (50ft)", "ref_HDS_L05SP1TS1_cont50ft"],
         ["Sim Water Surface L5 - Contour 5 ft Interval", "ref_HDS_L05SP1TS1_cont5ft"]],
        ['CRH_Map83_Simulated_POT_Surface_Model_L5_2009',
         ["Sim Water Surface L5 -Index Contour (50ft)", "ref_HDS_L05SP2TS1_cont50ft"],
         ["Sim Water Surface L5 - Contour 5 ft Interval","ref_HDS_L05SP2TS1_cont5ft"]]
        ]
for prop in properties:
    mxdname = (prop[0] + '.mxd')
    mxd = arcpy.mapping.MapDocument(TEMPLATEDIR + mxdname)
    print ("updating {}".format(mxdname))
    lyrList = arcpy.mapping.ListLayers(mxd)
    for lyr in lyrList:
        if lyr.name==prop[1][0]:
            print ("updating layer {}".format(lyr.name))
            arcpy.mapping.Layer.replaceDataSource(lyr, gdb, "FILEGDB_WORKSPACE", prop[1][1])
        elif lyr.name==prop[2][0]:
            print ("updating layer {}".format(lyr.name))
            arcpy.mapping.Layer.replaceDataSource(lyr, gdb, "FILEGDB_WORKSPACE", prop[2][1])
    arcpy.mapping.ExportToJPEG(mxd, os.path.join(dir_figs, (prop[0]+'.jpg')), resolution=300)
    mxd.saveACopy(os.path.join(dir_GIS, mxdname), ARCFILEVERSION)


maps_HH = ["CRH_Map84_ResidualsHH_Feet_Model_L1_2001",
          "CRH_Map89_ResidualsHH_Feet_Model_L5_2009",
          "CRH_Map88_ResidualsHH_Feet_Model_L5_2001",
          "CRH_Map87_ResidualsHH_Feet_Model_L3_2009",
          "CRH_Map86_ResidualsHH_Feet_Model_L3_2001",
          "CRH_Map85_ResidualsHH_Feet_Model_L1_2009"]
for mapname in maps_HH:
    mxdname = (mapname + '.mxd')
    mxd = arcpy.mapping.MapDocument(TEMPLATEDIR + mxdname)
    print ("updating {}".format(mxdname))
    yy = mapname.split('_')[-1]
    lyrList = arcpy.mapping.ListLayers(mxd)
    for lyr in lyrList:
        if lyr.name[:5]=="Water":
            print ("updating layer {}".format(lyr.name))
            arcpy.mapping.Layer.replaceDataSource(lyr, gdb, "FILEGDB_WORKSPACE", simnam+"_WL_targets_"+yy)
    arcpy.mapping.ExportToJPEG(mxd, os.path.join(dir_figs, (mapname+'.jpg')), resolution=300)
    mxd.saveACopy(os.path.join(dir_GIS, mxdname), ARCFILEVERSION)


maps_VHD_L1L3 = ["CRH_Map97_ResidualsVHD_Feet_Model_Layers_1_and_3_2001",
             "CRH_Map98_ResidualsVHD_Feet_Model_Layers_1_and_3_2009"]
for mapname in maps_VHD_L1L3:
    mxdname = (mapname + '.mxd')
    mxd = arcpy.mapping.MapDocument(TEMPLATEDIR + mxdname)
    print ("updating {}".format(mxdname))
    yy = mapname.split('_')[-1]
    lyrList = arcpy.mapping.ListLayers(mxd)
    for lyr in lyrList:
        if lyr.name[:3]=="VHD":
            print ("updating layer {}".format(lyr.name))
            arcpy.mapping.Layer.replaceDataSource(lyr, gdb, "FILEGDB_WORKSPACE", simnam+"_VHD_L1L3_targets_"+yy)
        elif lyr.name[:8]=="Residual":
            print ("updating layer {}".format(lyr.name))
            arcpy.mapping.Layer.replaceDataSource(lyr, gdb, "FILEGDB_WORKSPACE", simnam+"_VHD_L1L3_targets_"+yy)
    arcpy.mapping.ExportToJPEG(mxd, os.path.join(dir_figs, (mapname+'.jpg')), resolution=300)
    mxd.saveACopy(os.path.join(dir_GIS, mxdname), ARCFILEVERSION)


maps_VHD_L3L5 = ["CRH_Map100_ResidualsVHD_Feet_Model_Layers_3_and_5_2009",
             "CRH_Map99_ResidualsVHD_Feet_Model_Layers_3_and_5_2001"]
for mapname in maps_VHD_L3L5:
    mxdname = (mapname + '.mxd')
    mxd = arcpy.mapping.MapDocument(TEMPLATEDIR + mxdname)
    print ("updating {}".format(mxdname))
    yy = mapname.split('_')[-1]
    lyrList = arcpy.mapping.ListLayers(mxd)
    for lyr in lyrList:
        if lyr.name[:3]=="VHD":
            print ("updating layer {}".format(lyr.name))
            arcpy.mapping.Layer.replaceDataSource(lyr, gdb, "FILEGDB_WORKSPACE", simnam+"_VHD_L3L5_targets_"+yy)
        elif lyr.name[:8]=="Residual":
            print ("updating layer {}".format(lyr.name))
            arcpy.mapping.Layer.replaceDataSource(lyr, gdb, "FILEGDB_WORKSPACE", simnam+"_VHD_L3L5_targets_"+yy)
    arcpy.mapping.ExportToJPEG(mxd, os.path.join(dir_figs, (mapname+'.jpg')), resolution=300)
    mxd.saveACopy(os.path.join(dir_GIS, mxdname), ARCFILEVERSION)


maps_HHDs = ["CRH_Map106_ResidualsHHD_Feet_Model_L3_2009",
             "CRH_Map105_ResidualsHHD_Feet_Model_L3_2001"]
for mapname in maps_HHDs:
    mxdname = (mapname + '.mxd')
    mxd = arcpy.mapping.MapDocument(TEMPLATEDIR + mxdname)
    print ("updating {}".format(mxdname))
    yy = mapname.split('_')[-1]
    lyrList = arcpy.mapping.ListLayers(mxd)
    for lyr in lyrList:
        if lyr.name[:3]=="HHD":
            print ("updating layer {}".format(lyr.name))
            arcpy.mapping.Layer.replaceDataSource(lyr, gdb, "FILEGDB_WORKSPACE", simnam+"_HHD_L3_targets_"+yy)
        elif lyr.name[:8]=="Residual":
            print ("updating layer {}".format(lyr.name))
            arcpy.mapping.Layer.replaceDataSource(lyr, gdb, "FILEGDB_WORKSPACE", simnam+"_HHD_L3_targets_"+yy)
    arcpy.mapping.ExportToJPEG(mxd, os.path.join(dir_figs, (mapname+'.jpg')), resolution=300)
    mxd.saveACopy(os.path.join(dir_GIS, mxdname), ARCFILEVERSION)


maps_fld = ["CRH_Map144_HeightSimWT_above_LS_FT_2001",
            "CRH_Map145_HeightSimWT_above_LS_FT_2009",
            "CRH_Map146_Difference_HeightSim_WT_above_LS_FT_Pumps-Off_to2009"]
for mapname in maps_fld:
    mxdname = (mapname + '.mxd')
    mxd = arcpy.mapping.MapDocument(TEMPLATEDIR + mxdname)
    print ("updating {}".format(mxdname))
    lyrList = arcpy.mapping.ListLayers(mxd)
    for lyr in lyrList:
        if lyr.name[:6]=="Height":
            print ("updating layer {}".format(lyr.name))
            arcpy.mapping.Layer.replaceDataSource(lyr, gdb, "FILEGDB_WORKSPACE", "nfseg_props")
        elif lyr.name[:10]=="Difference": 
            print ("updating layer {}".format(lyr.name))
            arcpy.mapping.Layer.replaceDataSource(lyr, gdb, "FILEGDB_WORKSPACE", "nfseg_props_PUMPSOFF")
    arcpy.mapping.ExportToJPEG(mxd, os.path.join(dir_figs, (mapname+'.jpg')), resolution=300)
    mxd.saveACopy(os.path.join(dir_GIS, mxdname), ARCFILEVERSION)
