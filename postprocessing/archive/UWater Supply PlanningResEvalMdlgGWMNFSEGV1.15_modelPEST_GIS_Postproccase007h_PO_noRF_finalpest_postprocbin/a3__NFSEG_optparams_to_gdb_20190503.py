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


###basemap input (static)
base_gdb=cpath_py+"/templates/PEST_Baselayers.gdb"
ppts=['ppkx1_feet','ppkx3_feet','ppkx5_feet','ppkx7_feet','ppkz2_feet','ppkz4_feet','ppkz6_feet']

#find optimal parameters output file (*.pst.txt) - the rest of the files get named with the pst file name in it
num_simnams=0
for file in os.listdir(cpath_py_upper):
    if str(file[-4:])=='.pst':
        simnam=file[:-4]
        num_simnams=num_simnams+1
if num_simnams==0:
    print("looked for a *.pst.txt file - but found none :( - stopping")
    exit()
elif num_simnams>1:
    print("multiple *.pst.txt files found in this folder - stopping")
    exit()
else:
    print("sim name:"+str(simnam))
#read the pst file as lines
pst_file=cpath_py_upper+"/"+str(simnam)+".pst"
with open(pst_file, mode='r') as pst:
    pst_lines=pst.readlines()


#setup geodatabase based on simnam
gdb=cpath_py+"/"+simnam+".gdb"
if arcpy.Exists(gdb):
    print("geodatabase of this sim already exists - continuing ")
    #arcpy.Delete_management(gdb)#temp action for debugging
    #arcpy.CreateFileGDB_management(dir_sim_proc,simnam,"CURRENT")
    #exit()
else:
    arcpy.CreateFileGDB_management(cpath_py,simnam,"9.3")
    print("Output geodatabase set up")

##copy base pilot points layers into output gdb
for ppt in ppts:
    arcpy.Copy_management(base_gdb+"/"+ppt,gdb+"/"+ppt)
    arcpy.MakeFeatureLayer_management(gdb+"/"+ppt,ppt+"_view")

arcpy.CreateTable_management(gdb,"pst","#","#")
arcpy.MakeTableView_management(gdb+"/"+"pst","pst_view")
arcpy.AddField_management("pst_view","Name","TEXT","#","#","50","Name","NULLABLE","NON_REQUIRED","#")
arcpy.AddField_management("pst_view","Type1","TEXT","#","#","50","Type1","NULLABLE","NON_REQUIRED","#")
arcpy.AddField_management("pst_view","Type2","TEXT","#","#","50","Type2","NULLABLE","NON_REQUIRED","#")
arcpy.AddField_management("pst_view","Modeled","DOUBLE","#","#","#","Modeled","NULLABLE","NON_REQUIRED","#")
arcpy.AddField_management("pst_view","LOWER_BND","DOUBLE","#","#","#","LOWER_BND","NULLABLE","NON_REQUIRED","#")
arcpy.AddField_management("pst_view","UPPER_BND","DOUBLE","#","#","#","UPPER_BND","NULLABLE","NON_REQUIRED","#")
arcpy.AddField_management("pst_view","Group_","TEXT","#","#","50","Group_","NULLABLE","NON_REQUIRED","#")
arcpy.AddField_management("pst_view","VAL1","DOUBLE","#","#","#","VAL1","NULLABLE","NON_REQUIRED","#")
arcpy.AddField_management("pst_view","VAL2","DOUBLE","#","#","#","VAL2","NULLABLE","NON_REQUIRED","#")
arcpy.AddField_management("pst_view","VAL3","DOUBLE","#","#","#","VAL3","NULLABLE","NON_REQUIRED","#")

###populate pst_gdb table from the rei_lines
pst_fields = ['Name', 'Type1', 'Type2','Modeled','LOWER_BND','UPPER_BND','Group_', 'VAL1', 'VAL2', 'VAL3']

rd_flg=0
with arcpy.da.InsertCursor("pst_view",pst_fields) as cursor:
    read_flg=0
    for line in pst_lines:
        line=line[:-1]  # note that some is odd with way lines are read in...remove the last character in each line
        if line=="* observation groups":
            rd_flg=0
        if rd_flg==1:
            values=line.split()
            cursor.insertRow(values)
        if line=="* parameter data":  # this where the data to read begins
            rd_flg=1
            lc=0

###calculate "BND_FLG" field: = LOWER_BND when modeled value = LOWER_BND = UPPER_BND when modeled value = UPPER_BND
arcpy.SelectLayerByAttribute_management("pst_view","NEW_SELECTION","Modeled = LOWER_BND")
arcpy.CalculateField_management("pst_view","BND_FLG",'"'+"LOWER_BND"+'"',"PYTHON","#")
arcpy.SelectLayerByAttribute_management("pst_view","NEW_SELECTION","Modeled = UPPER_BND")
arcpy.CalculateField_management("pst_view","BND_FLG",'"'+"UPPER_BND"+'"',"PYTHON","#")

#join the pst_tbl to the copied ppt feature classes and export as a new fc (do once for each year 2001, 2009)
for ppt in ppts:
    arcpy.AddJoin_management(ppt+"_view","Name","pst_view","Name","KEEP_ALL")
    arcpy.SelectLayerByAttribute_management(ppt+"_view","NEW_SELECTION","pst.Name is not null")
    arcpy.FeatureClassToFeatureClass_conversion(ppt+"_view",gdb,simnam+"_"+ppt)
    arcpy.RemoveJoin_management(ppt+"_view","#")
    arcpy.SelectLayerByAttribute_management(ppt+"_view","CLEAR_SELECTION")
    arcpy.Delete_management(ppt+"_view")
    arcpy.Delete_management(gdb+"/"+ppt)

stop = time.clock()
DUR=round((stop-start)/60,1)
print("completed in "+str(DUR)+" min")
