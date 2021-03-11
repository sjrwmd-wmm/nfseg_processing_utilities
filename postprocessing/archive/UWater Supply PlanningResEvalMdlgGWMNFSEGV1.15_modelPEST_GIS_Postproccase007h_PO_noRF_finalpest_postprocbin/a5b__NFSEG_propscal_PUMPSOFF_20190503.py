import arcpy
import sys
import os
import struct
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

#######
###Inputs - must be located within cpath_py_upper directory

###basemap input (static)
base_gdb=cpath_py+"/templates/PEST_Baselayers.gdb"
nfseg_active_grid_poly=base_gdb+"/NFSEGActiveGrid_Albers_ROWCOL_LM"

file_DIS="nfseg.dis"
#file_RCH="nfseg.rch"
#file_EVT="nfseg.evt"
file_HDS="nfseg_PUMPSOFF.hds"

#template_mxd = arcpy.mapping.MapDocument(cpath_py +"/templates/nfseg_props_template.mxd")

#######
###MAIN

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

###get number of rows and columns from the DIS file
with open(cpath_py_upper+"/"+file_DIS,"r") as dis:
    firstline_dis=dis.readline()#repeat for number of commented-out lines
    #dis Dataset1
    secondline_dis=dis.readline()
    elements=secondline_dis.split()
    NLAY=elements[0]
    NROW=elements[1]
    NCOL=elements[2]
    #NPER=elements[3]
    print("number of rows: "+str(NROW))
    print("number of rows: "+str(NCOL))
    #read the Layer top/bottom elevations.  the LST file indicates the arrays are structured as:
    # L1Top L1Bot L2Bot L3Bot L4Bot L5Bot L6Bot L7Bot --> (NLAY + 1) arrays
    #first start w list of all row_cols  --> first item in array calld PROPS
    HEADER='"ROW_COL",'
    PROPS=[]
    for row in range(1,int(NROW)+1):
        curcol=0
        while curcol<(int(NCOL)):
            curcol=curcol+1
            PROPS.append(str(row)+"_"+str(curcol))
    #ignore next three lines DELR DELC
    thirdline_dis=dis.readline()
    fourthline_dis=dis.readline()
    fifthline_dis=dis.readline()
    #next read L1 Top
    HEADER=HEADER+'"L1Top",'
    iter_ct=0
    nextline_dis=dis.readline()#this line reads "       29   1.00000(10E20.12)                  -1     TOP of Model"
    for row in range(1,int(NROW)+1):
        curcol=0
        while curcol<(int(NCOL)):
            dataline=dis.readline()
            linevalues=dataline.split()
            for value in linevalues:
                curcol=curcol+1
                PROPS[iter_ct]=str(PROPS[iter_ct])+","+str(value)
                iter_ct=iter_ct+1
    #next read L1 Bot
    HEADER=HEADER+'"L1Bot",'
    iter_ct=0
    nextline_dis=dis.readline()#this line reads "        29   1.00000(10E20.12)                  -1     BOTTOM of Layer   1"
    for row in range(1,int(NROW)+1):
        curcol=0
        while curcol<(int(NCOL)):
            dataline=dis.readline()
            linevalues=dataline.split()
            for value in linevalues:
                curcol=curcol+1
                PROPS[iter_ct]=str(PROPS[iter_ct])+","+str(value)
                iter_ct=iter_ct+1
    #next read L2 Bot
    HEADER=HEADER+'"L2Bot",'
    iter_ct=0
    nextline_dis=dis.readline()#this line reads "        29   1.00000(10E20.12)                  -1     BOTTOM of Layer   2"
    for row in range(1,int(NROW)+1):
        curcol=0
        while curcol<(int(NCOL)):
            dataline=dis.readline()
            linevalues=dataline.split()
            for value in linevalues:
                curcol=curcol+1
                PROPS[iter_ct]=str(PROPS[iter_ct])+","+str(value)
                iter_ct=iter_ct+1
    #next read L3 Bot
    HEADER=HEADER+'"L3Bot",'
    iter_ct=0
    nextline_dis=dis.readline()#this line reads "        29   1.00000(10E20.12)                  -1     BOTTOM of Layer   3"
    for row in range(1,int(NROW)+1):
        curcol=0
        while curcol<(int(NCOL)):
            dataline=dis.readline()
            linevalues=dataline.split()
            for value in linevalues:
                curcol=curcol+1
                PROPS[iter_ct]=str(PROPS[iter_ct])+","+str(value)
                iter_ct=iter_ct+1
    #next read L4 Bot
    HEADER=HEADER+'"L4Bot",'
    iter_ct=0
    nextline_dis=dis.readline()#this line reads "        29   1.00000(10E20.12)                  -1     BOTTOM of Layer   4"
    for row in range(1,int(NROW)+1):
        curcol=0
        while curcol<(int(NCOL)):
            dataline=dis.readline()
            linevalues=dataline.split()
            for value in linevalues:
                curcol=curcol+1
                PROPS[iter_ct]=str(PROPS[iter_ct])+","+str(value)
                iter_ct=iter_ct+1
    #next read L5 Bot
    HEADER=HEADER+'"L5Bot",'
    iter_ct=0
    nextline_dis=dis.readline()#this line reads "        29   1.00000(10E20.12)                  -1     BOTTOM of Layer   5"
    for row in range(1,int(NROW)+1):
        curcol=0
        while curcol<(int(NCOL)):
            dataline=dis.readline()
            linevalues=dataline.split()
            for value in linevalues:
                curcol=curcol+1
                PROPS[iter_ct]=str(PROPS[iter_ct])+","+str(value)
                iter_ct=iter_ct+1
    #next read L6 Bot
    HEADER=HEADER+'"L6Bot",'
    iter_ct=0
    nextline_dis=dis.readline()#this line reads "        29   1.00000(10E20.12)                  -1     BOTTOM of Layer   6"
    for row in range(1,int(NROW)+1):
        curcol=0
        while curcol<(int(NCOL)):
            dataline=dis.readline()
            linevalues=dataline.split()
            for value in linevalues:
                curcol=curcol+1
                PROPS[iter_ct]=str(PROPS[iter_ct])+","+str(value)
                iter_ct=iter_ct+1
    #next read L7 Bot
    HEADER=HEADER+'"L7Bot",'
    iter_ct=0
    nextline_dis=dis.readline()#this line reads "        29   1.00000(10E20.12)                  -1     BOTTOM of Layer   7"
    for row in range(1,int(NROW)+1):
        curcol=0
        while curcol<(int(NCOL)):
            dataline=dis.readline()
            linevalues=dataline.split()
            for value in linevalues:
                curcol=curcol+1
                PROPS[iter_ct]=str(PROPS[iter_ct])+","+str(value)
                iter_ct=iter_ct+1
print("finished reading dis file")

#READ SOME NEW DATA 20171216
# read the Ibound inf files
for i in range(1,8):
    filename="ibound"+str(i)
    field="IBND"+str(i)
    HEADER=HEADER+'"'+field+'",'
    iter_ct=0
    with open(cpath_py_upper+"/"+str(filename)+".inf","r") as ref:
        for row in range(1,int(NROW)+1):
            curcol=0
            while curcol<(int(NCOL)):
                dataline=ref.readline()
                linevalues=dataline.split()
                for value in linevalues:
                    curcol=curcol+1
                    PROPS[iter_ct]=str(PROPS[iter_ct])+","+str(value)
                    iter_ct=iter_ct+1
print("finished reading Ibound inf files")

#******************
#HDS
#******************
if arcpy.Exists(cpath_py_upper+"/"+file_HDS):
    with open(cpath_py_upper+"/"+file_HDS, mode='rb') as file: ## b is important -> binary
        fileContent = file.read()
        print("using user-specied pumps off file /pest_postproc/nfseg_PUMPSOFF.hds")
elif arcpy.Exists(cpath_py_base+"/forward_runs/pumps_off/nfseg.hds"):
    with open(cpath_py_base+"/forward_runs/pumps_off/nfseg.hds", mode='rb') as file: ## b is important -> binary
        fileContent = file.read()
        print("using pumps off hds file found in : "+cpath_py_base+"/forward_runs/pumps_off/nfseg.hds")
else:
    print "Could not find the pumps off heads file /pest_postproc/nfseg_PUMPSOFF.hds or ../forward_runs/pumps_off/nfseg.hds - EXITING"
    exit()

##the hds file will contain arrays for each layer and each stress period indicated in the oc file
##read first array to get format
KSTP = struct.unpack("i", fileContent[:4])[0]
KPER = struct.unpack("i", fileContent[4:8])[0]
PERTIM = struct.unpack("f", fileContent[8:12])[0]
TOTIM = struct.unpack("f", fileContent[12:16])[0]
DESC_str = struct.unpack("cccccccccccccccc", fileContent[16:32])
DESC=""
for c in DESC_str:
    DESC=str(DESC)+c
DESC=DESC.strip()
#NCOL= struct.unpack("i", fileContent[32:36])[0]
#NROW= struct.unpack("i", fileContent[36:40])[0]
#ILAY= struct.unpack("i", fileContent[40:44])[0]
ARRAY_LEN = int(NCOL)*int(NROW)*4
BIN_LEN=len(fileContent)
N_ARRAYS = BIN_LEN / (ARRAY_LEN+44)
print("number of arrays in hds file: "+str(N_ARRAYS))
curpos=0
for i in range(1,N_ARRAYS+1):
    KSTP = struct.unpack("i", fileContent[curpos:curpos+4])[0]
    KPER = struct.unpack("i", fileContent[curpos+4:curpos+8])[0]
    PERTIM = struct.unpack("f", fileContent[curpos+8:curpos+12])[0]
    TOTIM = struct.unpack("f", fileContent[curpos+12:curpos+16])[0]
    DESC_str = struct.unpack("cccccccccccccccc", fileContent[curpos+16:curpos+32])
    DESC=""
    for c in DESC_str:
        DESC=str(DESC)+c
    DESC=DESC.strip()
    NCOL= struct.unpack("i", fileContent[curpos+32:curpos+36])[0]
    NROW= struct.unpack("i", fileContent[curpos+36:curpos+40])[0]
    ILAY= struct.unpack("i", fileContent[curpos+40:curpos+44])[0]
    print("reading data for SP:"+str(KPER)+" TS:"+str(KSTP)+" "+str(DESC)+" Layer:"+str(ILAY))
    curpos=curpos+44
    HEADER=HEADER+'"HDS_L'+'{0:02d}'.format(ILAY)+'SP'+str(KPER)+'TS'+str(KSTP)+'",'
    iter_ct=0
    for r in  range(1,NROW+1):
        for c in range(1,NCOL+1):
            VAL = struct.unpack("f", fileContent[curpos:curpos+4])[0]
            curpos=curpos+4
            value=float(VAL)
            PROPS[iter_ct]=str(PROPS[iter_ct])+","+str(value)
            iter_ct=iter_ct+1
###calculations
print ("calculating drydepth, dtw, flooding for PUMPSOFF...")
HEADER=HEADER[:-1]
calcslist=['drydep01','drydep09','dtw01','dtw09','fld01','fld09']
for calc in calcslist:
    HEADER=HEADER+',"'+calc+'"'
#print(HEADER)
iter_ct=0
for propline in PROPS:
    vals=propline.split(",")
    ROW_COL = vals[0]
    L1Top = float(vals[1])
    L1Bot = float(vals[2])
    L2Bot = float(vals[3])
    L3Bot = float(vals[4])
    L4Bot = float(vals[5])
    L5Bot = float(vals[6])
    L6Bot = float(vals[7])
    L7Bot = float(vals[8])

    ib1= float(vals[9])
    ib2= float(vals[10])
    ib3= float(vals[11])
    ib4= float(vals[12])
    ib5= float(vals[13])
    ib6= float(vals[14])
    ib7= float(vals[15])

    HDS_L01SP1TS1= float(vals[16])
    HDS_L02SP1TS1= float(vals[17])
    HDS_L03SP1TS1= float(vals[18])
    HDS_L04SP1TS1= float(vals[19])
    HDS_L05SP1TS1= float(vals[20])
    HDS_L06SP1TS1= float(vals[21])
    HDS_L07SP1TS1= float(vals[22])
    HDS_L01SP2TS1= float(vals[23])
    HDS_L02SP2TS1= float(vals[24])
    HDS_L03SP2TS1= float(vals[25])
    HDS_L04SP2TS1= float(vals[26])
    HDS_L05SP2TS1= float(vals[27])
    HDS_L06SP2TS1= float(vals[28])
    HDS_L07SP2TS1= float(vals[29])

    #dry depth0109 calcs
    if ib1 == 1 and HDS_L01SP1TS1<L1Bot:
        drydep01=L1Bot-HDS_L01SP1TS1
    else:
        drydep01="0.00"
    if ib1 == 1 and HDS_L01SP2TS1<L1Bot:
        drydep09=L1Bot-HDS_L01SP2TS1
    else:
        drydep09="0.00"
    #depth to water 01/09
    if ib1 == 1 :
        dtw01 = L1Top - HDS_L01SP1TS1
        dtw09 = L1Top - HDS_L01SP2TS1
    else:
        dtw01 = "0.00"
        dtw09 = "0.00"
    #flooded depth 01/09
    if ib1 == 1 and dtw01<0:
        fld01=-dtw01
    else:
        fld01="0.00"
    if ib1 == 1 and dtw09<0:
        fld09=-dtw09
    else:
        fld09="0.00"

    PROPS[iter_ct]=str(PROPS[iter_ct])+","+str(drydep01)+","+str(drydep09)+","+str(dtw01)+","+str(dtw09)+","+str(fld01)+","+str(fld09)
    iter_ct=iter_ct+1


#output to a CSV table
iter_ct=0
with open(cpath_py+"/"+"ref_PUMPSOFF.csv","w") as propscsv:
    propscsv.write(str(HEADER)+'\n')
    for line in PROPS:
        iter_ct=iter_ct+1
        propsline=line.split(",")
        propscsv.write('"'+str(propsline[0])+'"')
        for prop in range(1,len(propsline)):
            propscsv.write(","+str(propsline[prop]))
        propscsv.write('\n')
print("tmp csv output created")

arcpy.TableToTable_conversion(cpath_py+"/"+"ref_PUMPSOFF.csv",gdb,"ref_PUMPSOFF")
arcpy.MakeTableView_management(gdb+"/"+"ref_PUMPSOFF","tbl_view")
arcpy.AddIndex_management("tbl_view","ROW_COL","ROW_COL","NON_UNIQUE","NON_ASCENDING")
print("tmp gdb table created")

arcpy.MakeFeatureLayer_management(nfseg_active_grid_poly,"shp_view")
arcpy.AddJoin_management("shp_view","ROW_COL","tbl_view","ROW_COL","KEEP_ALL")
arcpy.FeatureClassToFeatureClass_conversion("shp_view",gdb,"nfseg_props_PUMPSOFF")
arcpy.RemoveJoin_management("shp_view","#")
print("properties fc created")
print("cleaning up")
arcpy.Delete_management("shp_view")
arcpy.Delete_management("tbl_view")
arcpy.Delete_management(cpath_py+"/"+"ref_PUMPSOFF.csv")

#now compare change in flooding from pumps off to 2009
arcpy.MakeFeatureLayer_management(gdb+"/nfseg_props_PUMPSOFF","PUMPSOFF_props_view")
arcpy.MakeFeatureLayer_management(gdb+"/nfseg_props","props_view")
arcpy.AddField_management("PUMPSOFF_props_view","basefld09","DOUBLE")
arcpy.AddJoin_management("PUMPSOFF_props_view","NFSEGActiveGrid_Albers_ROWCOL_LM_ROW_COL","props_view",
                         "NFSEGActiveGrid_Albers_ROWCOL_LM_ROW_COL","KEEP_ALL")
arcpy.CalculateField_management("PUMPSOFF_props_view","nfseg_props_PUMPSOFF.basefld09","!nfseg_props.ref_fld09!","PYTHON")
arcpy.RemoveJoin_management("PUMPSOFF_props_view","#")
arcpy.AddField_management("PUMPSOFF_props_view","delta_fld09","DOUBLE")
arcpy.CalculateField_management("PUMPSOFF_props_view","delta_fld09","!ref_PUMPSOFF_fld09!-!basefld09!","PYTHON")

stop = time.clock()
DUR=round((stop-start)/60,1)
print("output: nfseg_props.shp in " + cpath_py )
print("completed in "+str(DUR)+" min")