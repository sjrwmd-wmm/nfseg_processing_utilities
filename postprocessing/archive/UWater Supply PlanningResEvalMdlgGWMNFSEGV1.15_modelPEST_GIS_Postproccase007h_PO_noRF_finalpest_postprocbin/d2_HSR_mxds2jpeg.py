## export all mxds within a folder to jpg files of the same name (resolution = 300 dpi)

import arcpy
import os

print("Exporting jpeg maps related to Hydrostratigraphic Related(HSR): L1 thru L7 Elevations and Thickness, Elevation FWSW TDS 10,000ppm.")

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

#automatic figures right from the templates_gdb - no updates
mxdnames = ["HSR_Map3_Elevation_TDSConcentration_Iso-Surface.mxd",
            "HSR_Map21_Map_Vertical_CrossSections.mxd",
            "HSR_Map22_Hydrostratigraphic_CrossSection_A-Aprime.mxd",
            "HSR_Map23_Hydrostratigraphic_CrossSection_B-Bprime.mxd",
            "HSR_Map24_Hydrostratigraphic_CrossSection_C-Cprime.mxd",
            "HSR_Map24a_Hydrostratigraphic_CrossSection_E-Eprime.mxd",
            "HSR_Map25_Hydrostratigraphic_CrossSection_D-Dprime.mxd",
            "HSR_Map26_Areas_IntermediateConfiningUnitPresence.mxd"]

for mxdname in mxdnames:
    print "reprinting "+mxdname
    mxd = arcpy.mapping.MapDocument(cpath_py +'/templates/'+mxdname)
    arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
    mxd.saveACopy(cpath_py+'/'+mxdname,"9.0")

#figures to be updated with model data
mxdnames_ReqUpd = ["HSR_Map4_TopElevation_L1_FT.mxd","HSR_Map5_BottomElevation_L1_FT.mxd",
                   "HSR_Map6_Thickness_L1_FT.mxd","HSR_Map7_BottomElevation_L2_FT.mxd",
                   "HSR_Map8_Thickness_L2_FT.mxd","HSR_Map9_BottomElevation_L3_FT.mxd",
                   "HSR_Map10_Thickness_L3_FT.mxd","HSR_Map11_BottomElevation_L4_FT.mxd",
                   "HSR_Map12_Thickness_L4_FT.mxd","HSR_Map13_BottomElevation_L5_FT.mxd",
                   "HSR_Map14_Thickness_L5_FT.mxd","HSR_Map15_TopElevation_L6_FT.mxd",
                   "HSR_Map16_BottomElevation_L6_FT.mxd","HSR_Map17_Thickness_L6_FT.mxd",
                   "HSR_Map18_TopElevation_L7_FT.mxd","HSR_Map19_BottomElevation_L7_FT.mxd",
                   "HSR_Map20_Thickness_L7_FT.mxd"]

#HSR_Map4_TopElevation_L1
mxdname = 'HSR_Map4_TopElevation_L1_FT.mxd'
mxd = arcpy.mapping.MapDocument(cpath_py +'/templates/'+mxdname)
lyrList = arcpy.mapping.ListLayers(mxd)
for lyr in lyrList:
    if lyr.name[:3]=="Top":
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",'nfseg_props')
arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
mxd.saveACopy(cpath_py+'/'+mxdname,"9.0")
#"HSR_Map5_BottomElevation
mxdname = 'HSR_Map5_BottomElevation_L1_FT.mxd'
mxd = arcpy.mapping.MapDocument(cpath_py +'/templates/'+mxdname)
lyrList = arcpy.mapping.ListLayers(mxd)
for lyr in lyrList:
    if lyr.name[:4]=="Bott":
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",'nfseg_props')
arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
mxd.saveACopy(cpath_py+'/'+mxdname,"9.0")
#"HSR_Map6_Thickness_L1
mxdname = "HSR_Map6_Thickness_L1_FT.mxd"
mxd = arcpy.mapping.MapDocument(cpath_py +'/templates/'+mxdname)
lyrList = arcpy.mapping.ListLayers(mxd)
for lyr in lyrList:
    if lyr.name[:5]=="Layer":
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",'nfseg_props')
arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
mxd.saveACopy(cpath_py+'/'+mxdname,"9.0")
#HSR_Map7 L2 BOT
mxdname = "HSR_Map7_BottomElevation_L2_FT.mxd"
mxd = arcpy.mapping.MapDocument(cpath_py +'/templates/'+mxdname)
lyrList = arcpy.mapping.ListLayers(mxd)
for lyr in lyrList:
    if lyr.name[:4]=="Bott":
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",'nfseg_props')
arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
mxd.saveACopy(cpath_py+'/'+mxdname,"9.0")
#HSR_Map8 L2 thickness
mxdname = "HSR_Map8_Thickness_L2_FT.mxd"
mxd = arcpy.mapping.MapDocument(cpath_py +'/templates/'+mxdname)
lyrList = arcpy.mapping.ListLayers(mxd)
for lyr in lyrList:
    if lyr.name[:5]=="Layer":
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",'nfseg_props')
arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
mxd.saveACopy(cpath_py+'/'+mxdname,"9.0")
#HSR_Map9 L3 Bot
mxdname = "HSR_Map9_BottomElevation_L3_FT.mxd"
mxd = arcpy.mapping.MapDocument(cpath_py +'/templates/'+mxdname)
lyrList = arcpy.mapping.ListLayers(mxd)
for lyr in lyrList:
    if lyr.name[:4]=="Bott":
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",'nfseg_props')
arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
mxd.saveACopy(cpath_py+'/'+mxdname,"9.0")
#HSR_Map10 L3 thickness
mxdname = "HSR_Map10_Thickness_L3_FT.mxd"
mxd = arcpy.mapping.MapDocument(cpath_py +'/templates/'+mxdname)
lyrList = arcpy.mapping.ListLayers(mxd)
for lyr in lyrList:
    if lyr.name[:5]=="Layer":
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",'nfseg_props')
arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
mxd.saveACopy(cpath_py+'/'+mxdname,"9.0")
#HSR_Map11 L4 Bot
mxdname = "HSR_Map11_BottomElevation_L4_FT.mxd"
mxd = arcpy.mapping.MapDocument(cpath_py +'/templates/'+mxdname)
lyrList = arcpy.mapping.ListLayers(mxd)
for lyr in lyrList:
    if lyr.name[:4]=="Bott":
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",'nfseg_props')
arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
mxd.saveACopy(cpath_py+'/'+mxdname,"9.0")
#HSR_Map12 L4 thickness
mxdname = "HSR_Map12_Thickness_L4_FT.mxd"
mxd = arcpy.mapping.MapDocument(cpath_py +'/templates/'+mxdname)
lyrList = arcpy.mapping.ListLayers(mxd)
for lyr in lyrList:
    if lyr.name[:5]=="Layer":
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",'nfseg_props')
arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
mxd.saveACopy(cpath_py+'/'+mxdname,"9.0")
#HSR_Map13 L5 Bot
mxdname = "HSR_Map13_BottomElevation_L5_FT.mxd"
mxd = arcpy.mapping.MapDocument(cpath_py +'/templates/'+mxdname)
lyrList = arcpy.mapping.ListLayers(mxd)
for lyr in lyrList:
    if lyr.name[:4]=="Bott":
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",'nfseg_props')
arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
mxd.saveACopy(cpath_py+'/'+mxdname,"9.0")
#HSR_Map14 L5 thickness
mxdname = "HSR_Map14_Thickness_L5_FT.mxd"
mxd = arcpy.mapping.MapDocument(cpath_py +'/templates/'+mxdname)
lyrList = arcpy.mapping.ListLayers(mxd)
for lyr in lyrList:
    if lyr.name[:5]=="Layer":
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",'nfseg_props')
arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
mxd.saveACopy(cpath_py+'/'+mxdname,"9.0")
#HSR_Map15 L6 TOP
mxdname = "HSR_Map15_TopElevation_L6_FT.mxd"
mxd = arcpy.mapping.MapDocument(cpath_py +'/templates/'+mxdname)
lyrList = arcpy.mapping.ListLayers(mxd)
for lyr in lyrList:
    if lyr.name[:3]=="Top":
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",'nfseg_props')
arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
mxd.saveACopy(cpath_py+'/'+mxdname,"9.0")
#HSR_Map16 L6 Bot
mxdname = "HSR_Map16_BottomElevation_L6_FT.mxd"
mxd = arcpy.mapping.MapDocument(cpath_py +'/templates/'+mxdname)
lyrList = arcpy.mapping.ListLayers(mxd)
for lyr in lyrList:
    if lyr.name[:4]=="Bott":
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",'nfseg_props')
arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
mxd.saveACopy(cpath_py+'/'+mxdname,"9.0")
#HSR_Map17 L6 thickness
mxdname = "HSR_Map17_Thickness_L6_FT.mxd"
mxd = arcpy.mapping.MapDocument(cpath_py +'/templates/'+mxdname)
lyrList = arcpy.mapping.ListLayers(mxd)
for lyr in lyrList:
    if lyr.name[:5]=="Layer":
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",'nfseg_props')
arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
mxd.saveACopy(cpath_py+'/'+mxdname,"9.0")
#HSR_Map18 L7 TOP
mxdname = "HSR_Map18_TopElevation_L7_FT.mxd"
mxd = arcpy.mapping.MapDocument(cpath_py +'/templates/'+mxdname)
lyrList = arcpy.mapping.ListLayers(mxd)
for lyr in lyrList:
    if lyr.name[:3]=="Top":
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",'nfseg_props')
arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
mxd.saveACopy(cpath_py+'/'+mxdname,"9.0")
#HSR_Map19 L7 Bot
mxdname = "HSR_Map19_BottomElevation_L7_FT.mxd"
mxd = arcpy.mapping.MapDocument(cpath_py +'/templates/'+mxdname)
lyrList = arcpy.mapping.ListLayers(mxd)
for lyr in lyrList:
    if lyr.name[:4]=="Bott":
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",'nfseg_props')
arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
mxd.saveACopy(cpath_py+'/'+mxdname,"9.0")
#HSR_Map20 L7 thickness
mxdname = "HSR_Map20_Thickness_L7_FT.mxd"
mxd = arcpy.mapping.MapDocument(cpath_py +'/templates/'+mxdname)
lyrList = arcpy.mapping.ListLayers(mxd)
for lyr in lyrList:
    if lyr.name[:5]=="Layer":
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",'nfseg_props')
arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
mxd.saveACopy(cpath_py+'/'+mxdname,"9.0")

