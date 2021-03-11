## export all mxds within a folder to jpg files of the same name (resolution = 300 dpi)

import arcpy
import os

print("Exporting jpeg maps related to Boundary Condition Related (BCR): Active model boundary L3 thru 7, Recharge Rates, ET, Extinction Depths, Withdraws_Ag_PSCII_DSS.")

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


mxdnames_noupdate = ['BCR_Map27_Model_LateralBoundaries_L3.mxd',
            'BCR_Map28_Model_LateralBoundaries_L4.mxd',
            'BCR_Map29_Model_LateralBoundaries_L5.mxd',
            'BCR_Map30_Model_LateralBoundaries_L6.mxd',
            'BCR_Map31_Model_LateralBoundaries_L7.mxd',
            'BCR_Map32_NHDPlusV2_Flow-LineSub-Segments_RiverDrain-Package_Implementations.mxd',
            'BCR_Map33_PortionsNHD_Flowlines_Sub-Polygons_NFSEG_RiverPackage.mxd',
            'BCR_Map34_Gulf-of-Mexico_CoastalSwamps_RepresentedDrainPackage.mxd',
            'BCR_Map40_DistributionOf_Multi-AquiferWells.mxd',
            'BCR_Map41_DistributionOf_PSCIIWithdrawals_mgd_2001.mxd',
            'BCR_Map42_DistributionOf_PSCIIWithdrawals_mgd_2009.mxd',
            'BCR_Map43_DistributionOf_DSSWithdrawals_mgd.mxd',
            'BCR_Map44_DistributionOf_AgWithdrawals_mgd.mxd',
            'BCR_Map45_DistributionOf_Total_GW_WithdrawalsbyCounty_mgd_2001.mxd',
            'BCR_Map46_DistributionOf_Total_GW_WithdrawalsbyCounty_mgd_2009.mxd',
            'BCR_Map47_GroundwaterWithdrawals_by_County_and_Use_Type_mgd_2001.mxd',
            'BCR_Map48_GroundwaterWithdrawals_by_County_and_Use_Type_mgd_2009.mxd',
            'BCR_Map49_Location_RIBS_InjectionWells_Sinks_and_DrainageWells.mxd',
            'BCR_Map50_DistributionOf_SpecifiedHeads_by_GridCell.mxd']
for mxdname in mxdnames_noupdate:
    mxd = arcpy.mapping.MapDocument(cpath_py +'/templates/'+mxdname)
    arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
    mxd.saveACopy(cpath_py+'/'+mxdname,"9.0")

mxdnames_update_ETRCH = ['BCR_Map35_AssignedRechargeRates_ipy_2001.mxd',
                     'BCR_Map36_AssignedRechargeRates_ipy_2009.mxd',
                     'BCR_Map37_AssignedMaximumSaturatedET_Rates_ipy_2001.mxd',
                     'BCR_Map38_AssignedMaximumSaturatedET_Rates_ipy_2009.mxd',
                     'BCR_Map39_AssignedET_Extinction_Depths_FT.mxd']

for mxdname in mxdnames_update_ETRCH:
    mxd = arcpy.mapping.MapDocument(cpath_py +'/templates/'+mxdname)
    lyrList = arcpy.mapping.ListLayers(mxd)
    for lyr in lyrList:
        if lyr.name[:3]=="SIM":
            print "updating "+mxdname
            arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",'nfseg_props_ETRCHinp')
            arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
            mxd.saveACopy(cpath_py+'/'+mxdname,"9.0")

mxdnames_update_props = ['BCR_Map39_AssignedET_Extinction_Depths_FT.mxd']
for mxdname in mxdnames_update_props:
    mxd = arcpy.mapping.MapDocument(cpath_py +'/templates/'+mxdname)
    lyrList = arcpy.mapping.ListLayers(mxd)
    for lyr in lyrList:
        if lyr.name[:3]=="SIM":
            print "updating "+mxdname
            arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",'nfseg_props')
            arcpy.mapping.ExportToJPEG(mxd, dir_figs+'/'+mxdname[:-3]+'jpg', resolution=300)
            mxd.saveACopy(cpath_py+'/'+mxdname,"9.0")
