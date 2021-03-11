import arcpy
import sys
import os
import time
arcpy.env.overwriteOutput = True
start = time.clock()

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

gdb=cpath_py+"/"+simnam+"_ZB.gdb"
if arcpy.Exists(gdb):
    print("geodatabase for this sim exists - continuing ")
    #arcpy.Delete_management(gdb)#temp action for debugging
    #arcpy.CreateFileGDB_management(dir_sim_proc,simnam,"CURRENT")
    #exit()
else:
    arcpy.CreateFileGDB_management(cpath_py,simnam+"_ZB","9.3")
    print("geodatabase for this sim does not exist - creating one (ZB version")


### NOT USED YET template_mxd = arcpy.mapping.MapDocument(cpath_py + "/templates/nfseg_PEST_RIVDRN_flux.mxd")

###basemap input (static)
base_gdb=cpath_py+"/templates/PEST_Baselayers.gdb"
nfseg_active_grid_poly=base_gdb+"/NFSEGActiveGrid_Albers_ROWCOL_LM"

cbbcsv_fnames=['nfseg_all_to_cbc.cbc.2001.csv','nfseg_all_to_cbc.cbc.2009.csv']

#check to make sure the cbb csv files exist.
for file in cbbcsv_fnames:
    if arcpy.Exists(cpath_py+"/rerunCBB/water_budget_rerun/"+file) is False:
        print "no cbb csv files found in:"+(cpath_py+"/rerunCBB/"+file)
        print "MODFLOW rerun StepB must be run - exiting"
        exit()

###MAIN
arcpy.MakeFeatureLayer_management(nfseg_active_grid_poly,"grid_poly")
# get attribute info as lookup rowcol_lu
rowcol_lu_fields=['OBJECTID','row','column_','ROW_COL','Shape_Length','Shape_Area']
rowcol_lu={}
with arcpy.da.SearchCursor("grid_poly",rowcol_lu_fields)as cursor:
    for row in cursor:
        rowcol_lu[row[3]]=row
#print(rowcol_lu["162_539"])
print("finished creating rowcol attri lookup")
# get geometry info as lookup rowcol_poly_lu
rowcol_poly_lu={}
with arcpy.da.SearchCursor("grid_poly",["Shape@","ROW_COL"]) as cursor:
    for row in cursor:
        rowcol_poly_lu[row[1]]=row[0]
print("finished creating rowcol shape lookup")

### Read the file CBB.HEADER to get list of field names
HEADER_LIST=['Shape@','ROW_COL']
if os.path.isfile(cpath_py+"/rerunCBB/water_budget_rerun/"+"CBB.HEADER"):
    with open(cpath_py+"/rerunCBB/water_budget_rerun/"+"CBB.HEADER", mode='r') as filein:
        HEADER=filein.readline()
    HEADER_items=HEADER.split()
    for item in HEADER_items:
        HEADER_LIST.append(item)
else:
    print("did not find file CBB.HEADER in: "+cpath_py_upper)

file_ct=0
for cbbcsv in cbbcsv_fnames:
    print("processing: "+str(cbbcsv))
    ##output fc (grid cell polygons with mass balance results
    out_fc=cbbcsv.replace(".","_")
    arcpy.CreateFeatureclass_management(gdb,out_fc,"POLYGON","grid_poly")
    arcpy.MakeFeatureLayer_management(gdb+"/"+out_fc,"out_fc_view")
    arcpy.DefineProjection_management("out_fc_view","PROJCS['NAD_1983_Albers',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Albers'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-84.0],PARAMETER['Standard_Parallel_1',29.5],PARAMETER['Standard_Parallel_2',45.5],PARAMETER['Latitude_Of_Origin',23.0],UNIT['Meter',1.0]]")
    arcpy.DeleteField_management("out_fc_view","ROW")
    arcpy.DeleteField_management("out_fc_view","column_")
    ###Add CBB fields
    LongIntList=['CELLID','LAY','ROW','COL','IBOUND']
    for item in HEADER_items:
        #print(item)
        if item in LongIntList:
            arcpy.AddField_management("out_fc_view",item,"LONG","","","","","NULLABLE","NON_REQUIRED","")
        else:
            arcpy.AddField_management("out_fc_view",item,"DOUBLE","","","","","NULLABLE","NON_REQUIRED","")

    file_ct=file_ct+1
    #read data from cbbcsv and insert cursor
    with arcpy.da.InsertCursor("out_fc_view",HEADER_LIST) as cursor:
        with open(cpath_py+"/rerunCBB/water_budget_rerun/"+cbbcsv, mode='r') as filein:
            for cbbcsv_line in filein:
                #cbbcsv_line=filein.readline()
                cbbcsv_items=cbbcsv_line.split()
                csv_rowcol=str(cbbcsv_items[2])+"_"+str(cbbcsv_items[3])
                exp=[] 
                if csv_rowcol in rowcol_poly_lu:
                    exp.append(rowcol_poly_lu[csv_rowcol]) #  Shape (field from grid fc)
                    exp.append(csv_rowcol) #  ROW_COL (field from grid fc)
                    for val in cbbcsv_items:
                        exp.append(val)
                    cursor.insertRow(exp)
exit()

 
