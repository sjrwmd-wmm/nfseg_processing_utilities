## export all mxds within a folder to jpg files of the same name (resolution = 300 dpi)

import arcpy
import os

print("Exporting jpeg maps related to Special PEST Targets (OGR): Springsflows, baseflow, VHD/HHDs")

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


#mxdnames_noupdate = ['']
#for mxdname in mxdnames_noupdate:
#    mxd = arcpy.mapping.MapDocument(cpath_py +'/templates/'+mxdname)
#    arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)

##BEGIN FIGURES


mxdname = 'OGR_Map51_Location_and_RelativeMagnitudesSpring_DischargeRates_cfs_2001.mxd'
mxd = arcpy.mapping.MapDocument(cpath_py +'/templates/'+mxdname)
lyrList = arcpy.mapping.ListLayers(mxd)
for lyr in lyrList:
    if lyr.name[:3]=="Dis":
        print "updating "+mxdname
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",simnam+"_qsprings_2001")
arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
mxd.saveACopy(cpath_py+'/'+mxdname,"9.0")
mxdname = 'OGR_Map52_Location_and_RelativeMagnitudesSpring_DischargeRates_cfs_2009.mxd'
mxd = arcpy.mapping.MapDocument(cpath_py +'/templates/'+mxdname)
lyrList = arcpy.mapping.ListLayers(mxd)
for lyr in lyrList:
    if lyr.name[:3]=="Dis":
        print "updating "+mxdname
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",simnam+"_qsprings_2009")
arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
mxd.saveACopy(cpath_py+'/'+mxdname,"9.0")
mxdname = 'OGR_Map53_Magnitude-1Springs_and_SpringGroups_and_EstimatedFlowrates_cfs_2001.mxd'
mxd = arcpy.mapping.MapDocument(cpath_py +'/templates/'+mxdname)
lyrList = arcpy.mapping.ListLayers(mxd)
for lyr in lyrList:
    if lyr.name[:6]=="Spring":
        print "updating "+mxdname
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",simnam+"_qsprings_1st_2001")
arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
mxd.saveACopy(cpath_py+'/'+mxdname,"9.0")
mxdname = 'OGR_Map54_Magnitude-1Springs_and_SpringGroups_and_EstimatedFlowrates_cfs_2009.mxd'
mxd = arcpy.mapping.MapDocument(cpath_py +'/templates/'+mxdname)
lyrList = arcpy.mapping.ListLayers(mxd)
for lyr in lyrList:
    if lyr.name[:6]=="Spring":
        print "updated"+lyr.name
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",simnam+"_qsprings_1st_2009")
arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
mxd.saveACopy(cpath_py+'/'+mxdname,"9.0")
print "updated "+mxdname

QR_mxds = ["OGR_Map55_EstimatedBaseflowPickupFlowrates_cfs_RegionA_2001.mxd",
           "OGR_Map56_EstimatedBaseflowPickupFlowrates_cfs_RegionB_2001.mxd",
           "OGR_Map57_EstimatedBaseflowPickupFlowrates_cfs_RegionC_2001.mxd",
           "OGR_Map59_EstimatedBaseflowPickupFlowrates_cfs_RegionA_2009.mxd",
           "OGR_Map60_EstimatedBaseflowPickupFlowrates_cfs_RegionB_2009.mxd",
           "OGR_Map61_EstimatedBaseflowPickupFlowrates_cfs_RegionC_2009.mxd"]
for mxdname in QR_mxds:
    mxd = arcpy.mapping.MapDocument(cpath_py +'/templates/'+mxdname)
    lyrList = arcpy.mapping.ListLayers(mxd)
    for lyr in lyrList:
        if lyr.name[:4]=="Gage":
            print "updated"+lyr.name
            arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",simnam+"_qr_20012009")
    arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
    mxd.saveACopy(cpath_py+'/'+mxdname,"9.0")
    print "updated "+mxdname

QS_mxds = ["OGR_Map58_EstimatedCumulativeBaseflows_cfs_2001.mxd",
           "OGR_Map62_EstimatedCumulativeBaseflows_cfs_2009.mxd"]
for mxdname in QS_mxds:
    mxd = arcpy.mapping.MapDocument(cpath_py +'/templates/'+mxdname)
    lyrList = arcpy.mapping.ListLayers(mxd)
    for lyr in lyrList:
        if lyr.name[:4]=="Gage":
            print "updated"+lyr.name
            arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",simnam+"_qs_20012009")
        if lyr.name[:12]=="Contributing":
            print "updated"+lyr.name
            arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",simnam+"_qrqs_gagepoly_NCB")
    arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
    mxd.saveACopy(cpath_py+'/'+mxdname,"9.0")
    print "updated "+mxdname

#VHD mxds
mxdname = "OGR_Map63_VHD_FT_SAS_vsUFA_2001.mxd"
mxd = arcpy.mapping.MapDocument(cpath_py +'/templates/'+mxdname)
lyrList = arcpy.mapping.ListLayers(mxd)
for lyr in lyrList:
    if lyr.name[:6]=="Values":
        #print lyr.name
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",simnam+"_VHD_L1L3_targets_2001")
arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
mxd.saveACopy(cpath_py+'/'+mxdname,"9.0")
print "updated "+mxdname

mxdname = "OGR_Map64_VHD_FT_UFA_aquifer_vsUZLFA_2001.mxd"
mxd = arcpy.mapping.MapDocument(cpath_py +'/templates/'+mxdname)
lyrList = arcpy.mapping.ListLayers(mxd)
for lyr in lyrList:
    if lyr.name[:6]=="Values":
        #print lyr.name
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",simnam+"_VHD_L3L5_targets_2001")
arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
mxd.saveACopy(cpath_py+'/'+mxdname,"9.0")
print "updated "+mxdname

mxdname = "OGR_Map65_VHD_FT_SAS_vsUFA_2009.mxd"
mxd = arcpy.mapping.MapDocument(cpath_py +'/templates/'+mxdname)
lyrList = arcpy.mapping.ListLayers(mxd)
for lyr in lyrList:
    if lyr.name[:6]=="Values":
        #print lyr.name
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",simnam+"_VHD_L1L3_targets_2009")
arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
mxd.saveACopy(cpath_py+'/'+mxdname,"9.0")
print "updated "+mxdname

mxdname = "OGR_Map66_VHD_FT_UFA_aquifer_vsUZLFA_2009.mxd"
mxd = arcpy.mapping.MapDocument(cpath_py +'/templates/'+mxdname)
lyrList = arcpy.mapping.ListLayers(mxd)
for lyr in lyrList:
    if lyr.name[:6]=="Values":
        #print lyr.name
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",simnam+"_VHD_L3L5_targets_2009")
arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
mxd.saveACopy(cpath_py+'/'+mxdname,"9.0")
print "updated "+mxdname

#HHD mxds
#2001
mxdname = "OGR_Map67_HHD_FT_Upper_Floridan_aquifer_2001.mxd"
mxd = arcpy.mapping.MapDocument(cpath_py +'/templates/'+mxdname)
lyrList = arcpy.mapping.ListLayers(mxd)
for lyr in lyrList:
    if lyr.name[:3]=="HHD":
        print lyr.name
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",simnam+"_HHD_L3_targets_01")
arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
mxd.saveACopy(cpath_py+'/'+mxdname,"9.0")
print "updated "+mxdname
#2009
mxdname = "OGR_Map68_HHD_FT_Upper_Floridan_aquifer_2009.mxd"
mxd = arcpy.mapping.MapDocument(cpath_py +'/templates/'+mxdname)
lyrList = arcpy.mapping.ListLayers(mxd)
for lyr in lyrList:
    if lyr.name[:3]=="HHD":
        print lyr.name
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",simnam+"_HHD_L3_targets_09")
arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
mxd.saveACopy(cpath_py+'/'+mxdname,"9.0")
print "updated "+mxdname
