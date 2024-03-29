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

gdb=cpath_py+"/"+simnam+".gdb"
if arcpy.Exists(gdb):
    print("geodatabase for this sim exists - continuing ")
    #arcpy.Delete_management(gdb)#temp action for debugging
    #arcpy.CreateFileGDB_management(dir_sim_proc,simnam,"CURRENT")
    #exit()
else:
    arcpy.CreateFileGDB_management(cpath_py,simnam,"9.3")
    print("geodatabase for this sim does not exist - creating one")

template_mxd = arcpy.mapping.MapDocument(cpath_py + "/templates/nfseg_PEST_RIVDRN_flux.mxd")

file_LST="nfseg.lst"
with open(cpath_py_upper+"/"+file_LST, mode='r') as lst:
    lst_lines=lst.readlines()

#           DRAINS   PERIOD    1   STEP   1
#    RIVER LEAKAGE   PERIOD    1   STEP   1
#           DRAINS   PERIOD    2   STEP   1
#    RIVER LEAKAGE   PERIOD    2   STEP   1

###basemap input (static)
base_gdb=cpath_py+"/templates/PEST_Baselayers.gdb"
nfseg_active_grid_poly=base_gdb+"/NFSEGActiveGrid_Albers_ROWCOL_LM"

##output fc (grid cell polygons for RIV/DRN
out_fc="nfseg_lst_Q"

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

#print(rowcol_poly_lu["162_539"])
#set up a fc to put the lst q data in
arcpy.CreateFeatureclass_management(gdb,out_fc,"POLYGON","grid_poly")
arcpy.MakeFeatureLayer_management(gdb+"/"+out_fc,"out_fc_view")
arcpy.DefineProjection_management("out_fc_view","PROJCS['NAD_1983_Albers',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Albers'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-84.0],PARAMETER['Standard_Parallel_1',29.5],PARAMETER['Standard_Parallel_2',45.5],PARAMETER['Latitude_Of_Origin',23.0],UNIT['Meter',1.0]]")
arcpy.AddField_management("out_fc_view","ROW","SHORT","","","","","NULLABLE","NON_REQUIRED","")
arcpy.AddField_management("out_fc_view","COL","SHORT","","","","","NULLABLE","NON_REQUIRED","")
#Error ROW_COL field already exists
#arcpy.AddField_management("out_fc_view","ROW_COL","TEXT","#","#","10","ROW_COL","NULLABLE","NON_REQUIRED","#")
arcpy.AddField_management("out_fc_view","STRSSPER","SHORT","","","","","NULLABLE","NON_REQUIRED","")
arcpy.AddField_management("out_fc_view","TIMESTEP","SHORT","","","","","NULLABLE","NON_REQUIRED","")
arcpy.AddField_management("out_fc_view","TYPE","TEXT","#","#","10","TYPE","NULLABLE","NON_REQUIRED","#")
arcpy.AddField_management("out_fc_view","REACH","LONG","","","","","NULLABLE","NON_REQUIRED","")
arcpy.AddField_management("out_fc_view","LAYER","SHORT","","","","","NULLABLE","NON_REQUIRED","")
arcpy.AddField_management("out_fc_view","LRC","TEXT","#","#","15","LRC","NULLABLE","NON_REQUIRED","#")
arcpy.AddField_management("out_fc_view","RATE_CFS","DOUBLE","","","","","NULLABLE","NON_REQUIRED","")

rd_flg="OFF"
ctr=0
lc=0
with arcpy.da.InsertCursor("out_fc_view",['Shape@','ROW_COL','ROW','COL','STRSSPER','TIMESTEP','TYPE','REACH','LAYER','LRC','RATE_CFS']) as cursor:
    for line in lst_lines:
        lc=lc+1
        exp=[]
        ###by default it will start by not reading the data
        if rd_flg<>"OFF" and len(line)>1:
            ctr=ctr+1
            items=line.split()
            ROWCOL=str(items[5])+"_"+str(items[7])
            exp=[] 
            exp.append(rowcol_poly_lu[ROWCOL]) #  Shape
            exp.append(ROWCOL) #  ROWCOL
            exp.append(rowcol_lu[ROWCOL][1]) #  ROW
            exp.append(rowcol_lu[ROWCOL][2]) #  COL
            exp.append(SP) #  Stress Period
            exp.append(TS) #  Time Step
            exp.append(rd_flg) #  TYPE
            exp.append(items[1]) #  REACH
            exp.append(items[3]) #  LAYER
            exp.append(str(items[3])+"_"+str(items[5])+"_"+str(items[7])) #  LRC
            exp.append(float(items[9])/86400) #  RATE converts cfd to cfs
            cursor.insertRow(exp)
             
        ###check for flags used to start reading the data
        if len(line)<2:
            rd_flg="OFF" # use to reset read flag in between groups of data
        if len(line)>30 and line[:30]=='           DRAINS   PERIOD    ':
            SP=line[30:31] # SP
            TS=line[41:42] # TS
            rd_flg="DRN"
        if len(line)>30 and line[:30]=='    RIVER LEAKAGE   PERIOD    ':
            SP=line[30:31] # SP
            TS=line[41:42] # TS
            rd_flg="RIV" 


#force stop to prevent auto-figures from being generated...
exit()

###fc completed, now update map figures
eleList = arcpy.mapping.ListLayoutElements(template_mxd, "TEXT_ELEMENT")
for ele in eleList:
    if ele.text == "SIMNAM":
        ele.text = str(simnam)

LayList = arcpy.mapping.ListLayers(template_mxd)
for lyr in LayList:
    if lyr.name=="DRN Flux - 2001":
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,'FILEGDB_WORKSPACE',out_fc)
        lyr.visible = True
        for ele in eleList:
            if ele.text == 'FIGNAME':
                ele.text = "DRN Boundary Flux - 2001"
                arcpy.mapping.ExportToJPEG(template_mxd,cpath_py +"/"+simnam+"_DRN_Q_2001.jpeg")
                ele.text = "FIGNAME"
        lyr.visible = False
    if lyr.name=="DRN Flux - 2009":
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,'FILEGDB_WORKSPACE',out_fc)
        lyr.visible = True
        for ele in eleList:
            if ele.text == 'FIGNAME':
                ele.text = "DRN Boundary Flux - 2009"
                arcpy.mapping.ExportToJPEG(template_mxd,cpath_py +"/"+simnam+"_DRN_Q_2009.jpeg")
                ele.text = "FIGNAME"
        lyr.visible = False
    if lyr.name=="RIV Flux - 2001":
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,'FILEGDB_WORKSPACE',out_fc)
        lyr.visible = True
        for ele in eleList:
            if ele.text == 'FIGNAME':
                ele.text = "RIV Boundary Flux - 2001"
                arcpy.mapping.ExportToJPEG(template_mxd,cpath_py +"/"+simnam+"_RIV_Q_2001.jpeg")
                ele.text = "FIGNAME"
        lyr.visible = False
    if lyr.name=="RIV Flux - 2009":
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,'FILEGDB_WORKSPACE',out_fc)
        lyr.visible = True
        for ele in eleList:
            if ele.text == 'FIGNAME':
                ele.text = "RIV Boundary Flux - 2009"
                arcpy.mapping.ExportToJPEG(template_mxd,cpath_py +"/"+simnam+"_RIV_Q_2009.jpeg")
                ele.text = "FIGNAME"
        lyr.visible = False
    if lyr.name=="RIV&DRN Flux - 2001":
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,'FILEGDB_WORKSPACE',out_fc)
        lyr.visible = True
        for ele in eleList:
            if ele.text == 'FIGNAME':
                ele.text = "RIV&DRN Boundary Flux - 2001"
                arcpy.mapping.ExportToJPEG(template_mxd,cpath_py +"/"+simnam+"_RIVDRN_Q_2001.jpeg")
                ele.text = "FIGNAME"
        lyr.visible = False
    if lyr.name=="RIV&DRN Flux - 2009":
        arcpy.mapping.Layer.replaceDataSource(lyr,gdb,'FILEGDB_WORKSPACE',out_fc)
        lyr.visible = True
        for ele in eleList:
            if ele.text == 'FIGNAME':
                ele.text = "RIV&DRN Boundary Flux - 2009"
                arcpy.mapping.ExportToJPEG(template_mxd,cpath_py +"/"+simnam+"_RIVDRN_Q_2009.jpeg")
                ele.text = "FIGNAME"
        lyr.visible = False
template_mxd.saveACopy(cpath_py + "/"+simnam+"_PEST_RIVDRN_flux.mxd","10.0")
