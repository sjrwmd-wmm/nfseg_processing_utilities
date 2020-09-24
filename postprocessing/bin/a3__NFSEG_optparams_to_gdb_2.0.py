import arcpy
import sys
import os

import time
arcpy.env.overwriteOutput = True
start = time.clock()

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


# Get the working PATHs
cpath_py, cpath_py_upper, cpath_py_base = myut.get_current_PATHs()

print("current directory: " + str(cpath_py))
print("parent directory: " + str(cpath_py_upper))
print("grandparent directory: " + str(cpath_py_base))


###basemap input (static)
base_gdb = (TEMPLATEDIR + "PEST_Baselayers.gdb")
#base_gdb=cpath_py+"/templates/PEST_Baselayers.gdb"
ppts=['ppkx1_feet','ppkx3_feet','ppkx5_feet','ppkx7_feet','ppkz2_feet','ppkz4_feet','ppkz6_feet']


# Find PEST optimal parameters output file (*.pst) in the parent directory
# and get the basename to attach to output files generated by this script
simnam = myut.get_unique_filebasename_from_suffix(cpath_py_upper,'.pst')
print("sim name: "+str(simnam))


#setup geodatabase based on simnam
gdb=cpath_py+"/"+simnam+".gdb"
if arcpy.Exists(gdb):
    print("geodatabase of this sim already exists - continuing ")
    #arcpy.Delete_management(gdb)#temp action for debugging
    #arcpy.CreateFileGDB_management(dir_sim_proc,simnam,"CURRENT")
    #exit()
else:
    arcpy.CreateFileGDB_management(cpath_py,simnam, ARCFILEVERSION)
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
arcpy.AddField_management("pst_view","BND_FLG","TEXT","#","#","10","BND_FLG","NULLABLE","NON_REQUIRED","#")


###populate pst_gdb table from the rei_lines
pst_fields = ['Name', 'Type1', 'Type2','Modeled','LOWER_BND','UPPER_BND','Group_', 'VAL1', 'VAL2', 'VAL3']

#rd_flg=0
#with arcpy.da.InsertCursor("pst_view",pst_fields) as cursor:
#    read_flg=0
#    for line in pst_lines:
#        line=line[:-1]  # note that some is odd with way lines are read in...remove the last character in each line
#        if line=="* observation groups":
#            rd_flg=0
#        if rd_flg==1:
#            values=line.split()
#            if len(values)==len(pst_fields):  #  !!!PMB!!! temporary check
#                #print(values)  #  !!!PMB!!! temporary print statement
#                cursor.insertRow(values)
#        if line=="* parameter data":  # this where the data to read begins
#            rd_flg=1
#            lc=0
#read the pst file as lines
pst_file=cpath_py_upper+"/"+str(simnam)+".pst"
#read_flg=False
with arcpy.da.InsertCursor("pst_view",pst_fields) as cursor:
    
    read_flg=False # Initialize the read flag to "False"
    
    with open((cpath_py_upper+"/"+str(simnam)+".pst"), 'r') as pst:
        for line in pst:
            
            # Remove any potential end of line characters
            line = line.strip()
            
            # !!!PMB likely not needed, 20190719!!! note that some is odd with way lines are read in...remove the last character in each line
            #line=line[:-1]
            
            values = line.split()
            
            # Set the read_flg according to whether we are in the right section
            if values[0]=="*":
                if (" ".join(values[1:])=="parameter data"): read_flg=True
                else: read_flg=False
            #
            if read_flg:
                # Check whether the line has the correct number of fields
                if len(values)==len(pst_fields):
                    #print(values)  #  !!!PMB!!! debugging print statement
                    cursor.insertRow(values)
                #
            # END if over read_flg
        # close file
# END pst_lines

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
