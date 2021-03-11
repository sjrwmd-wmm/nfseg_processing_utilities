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
file_RCH="nfseg.rch"
file_EVT="nfseg.evt"
file_HDS="nfseg.hds"

template_mxd = arcpy.mapping.MapDocument(cpath_py +"/templates/nfseg_props_template.mxd")

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
    print("number of cols: "+str(NCOL))
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
    #print(PROPS[0])
    #print(PROPS[iter_ct-1])
print("finished reading dis file")

###attributes we want carried over - in order they will appear in output, must have a *.ref file of same name (e.g. kx1.ref
propslist=['kx1', 'kx2', 'kx3', 'kx4', 'kx5', 'kx6', 'kx7', 'kz1', 'kz2', 'kz3', 'kz4', 'kz5', 'kz6', 'kz7']
# read the props ref files
for field in propslist:
    #print(field)
    HEADER=HEADER+'"'+field+'",'
    #print("preps complete")
    iter_ct=0
    with open(cpath_py_upper+"/"+str(field)+".ref","r") as ref:
        for row in range(1,int(NROW)+1):
            curcol=0
            while curcol<(int(NCOL)):
                dataline=ref.readline()
                linevalues=dataline.split()
                for value in linevalues:
                    curcol=curcol+1
                    PROPS[iter_ct]=str(PROPS[iter_ct])+","+str(value)
                    iter_ct=iter_ct+1
print("finished reading ref files")
#print(HEADER)

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

#********
#RECHARGE - requires a fixed format 
#********
with open(cpath_py_upper+"/"+file_RCH,"r") as RCH:
    RCH_lines=[]
    for line in RCH.readlines():
        RCH_lines.append(line.strip())
#2001 - expecting to see RCH_lines[4]  as extrnal array files=signaled by "OPEN/CLOSE"
if RCH_lines[4][:10]<>"OPEN/CLOSE":
    print "Stopping: RCH file format change 2001.  check:", cpath_py_upper+"/"+file_RCH
    exit()
line_items=RCH_lines[4].split()
rcharray=line_items[1]
rcharray=cpath_py_upper+"/"+rcharray.strip("'")
if os.path.isfile(rcharray) is False:
    print ("stopping did not find the 2001 rcharray:",rcharray)
    exit()
with open(rcharray, "r") as extrch:
    HEADER=HEADER+'"RCH01",'
    iter_ct=0
    for row in range(1,int(NROW)+1):
        curcol=0
        while curcol<(int(NCOL)):
            dataline=extrch.readline()
            linevalues=dataline.split()
            for value in linevalues:
                curcol=curcol+1
                PROPS[iter_ct]=str(PROPS[iter_ct])+","+str(value)
                iter_ct=iter_ct+1
print("finished reading RCH 01 ext file:  " + rcharray)
#2009 - expecting to see RCH_lines[6]  as extrnal array files=signaled by "OPEN/CLOSE"
if RCH_lines[6][:10]<>"OPEN/CLOSE":
    print "Stopping: RCH file format change 2009.  check:", cpath_py_upper+"/"+file_RCH
    exit()
line_items=RCH_lines[6].split()
rcharray=line_items[1]
rcharray=cpath_py_upper+"/"+rcharray.strip("'")
if os.path.isfile(rcharray) is False:
    print ("stopping did not find the 2009 rcharray:",rcharray)
    exit()
with open(rcharray, "r") as extrch:
    HEADER=HEADER+'"RCH09",'
    iter_ct=0
    for row in range(1,int(NROW)+1):
        curcol=0
        while curcol<(int(NCOL)):
            dataline=extrch.readline()
            linevalues=dataline.split()
            for value in linevalues:
                curcol=curcol+1
                PROPS[iter_ct]=str(PROPS[iter_ct])+","+str(value)
                iter_ct=iter_ct+1
print("finished reading RCH 09 ext file:  " + rcharray)

#******************
#EVAPOTRANSPIRATION - requires a fixed format 
#******************
with open(cpath_py_upper+"/"+file_EVT,"r") as EVT:
    EVT_lines=[]
    for line in EVT.readlines():
        EVT_lines.append(line.strip())
#2001 ET Surface
if EVT_lines[4][:57]<>"20   1.00000(10e20.12)                  -1     ET SURFACE":
    print "Stopping: EVT file format change at ETSURF01.  check:", cpath_py_upper+"/"+file_EVT
    exit()
ctr=4
HEADER=HEADER+'"ETSURF",'
iter_ct=0
for row in range(1,int(NROW)+1):
    curcol=0
    while curcol<(int(NCOL)):
        ctr=ctr+1
        dataline=EVT_lines[ctr]
        linevalues=dataline.split()
        for value in linevalues:
            curcol=curcol+1
            PROPS[iter_ct]=str(PROPS[iter_ct])+","+str(value)
            iter_ct=iter_ct+1
print("finished reading ET SURFACE 01 array from:  "+file_EVT)
#2001 ET rate
ctr=ctr+1
if EVT_lines[ctr][:10]<>"OPEN/CLOSE": #e.g., OPEN/CLOSE" 'evt_rate_after_mul_2001.ref'  1
    print "Stopping: file format change at EVT Rate 01.  check:", cpath_py_upper+"/"+file_EVT
    exit()
line_items=EVT_lines[ctr].split()
evtarray=line_items[1]
evtarray=cpath_py_upper+"/"+evtarray.strip("'")
if os.path.isfile(evtarray) is False:
    print ("stopping did not find the 2001 evt rate array:"+evtarray)
    exit()
with open(evtarray, "r") as extevt:
    HEADER=HEADER+'"ETRATE01",'
    iter_ct=0
    for row in range(1,int(NROW)+1):
        curcol=0
        while curcol<(int(NCOL)):
            dataline=extevt.readline()
            linevalues=dataline.split()
            for value in linevalues:
                curcol=curcol+1
                PROPS[iter_ct]=str(PROPS[iter_ct])+","+str(value)
                iter_ct=iter_ct+1
print("finished reading ETRATE 01 ext file:  " + evtarray)
#2001 EXT Depth
ctr=ctr+1
if EVT_lines[ctr][:55]<>"20   1.00000(10e20.12)                  -1     ET DEPTH":
    print "Stopping: EVT file format change at 01 EXTD.  check:", cpath_py_upper+"/"+file_EVT
    exit()
HEADER=HEADER+'"EXTD01",'
iter_ct=0
for row in range(1,int(NROW)+1):
    curcol=0
    while curcol<(int(NCOL)):
        ctr=ctr+1
        dataline=EVT_lines[ctr]
        linevalues=dataline.split()
        for value in linevalues:
            curcol=curcol+1
            PROPS[iter_ct]=str(PROPS[iter_ct])+","+str(value)
            iter_ct=iter_ct+1
print("finished reading ET 01 Extinction Depth array from:  "+file_EVT)
#2009 ET Surface --> expecting to see  -1 1 1 -1 meaning no change from 2001
ctr=ctr+1
if EVT_lines[ctr][:9]<>"-1 1 1 -1":
    print "Stopping: EVT file format change at ETSURF09.  check:", cpath_py_upper+"/"+file_EVT
    exit()
#2009 ET Rate --> 
ctr=ctr+1
if EVT_lines[ctr][:10]<>"OPEN/CLOSE": #e.g., OPEN/CLOSE" 'evt_rate_after_mul_2001.ref'  1
    print "Stopping: file format change at EVT Rate 09.  check:", cpath_py_upper+"/"+file_EVT
    exit()
line_items=EVT_lines[ctr].split()
evtarray=line_items[1]
evtarray=cpath_py_upper+"/"+evtarray.strip("'")
if os.path.isfile(evtarray) is False:
    print ("stopping did not find the 2009 evt rate array:"+evtarray)
    exit()
with open(evtarray, "r") as extevt:
    HEADER=HEADER+'"ETRATE09",'
    iter_ct=0
    for row in range(1,int(NROW)+1):
        curcol=0
        while curcol<(int(NCOL)):
            dataline=extevt.readline()
            linevalues=dataline.split()
            for value in linevalues:
                curcol=curcol+1
                PROPS[iter_ct]=str(PROPS[iter_ct])+","+str(value)
                iter_ct=iter_ct+1
print("finished reading ETRATE 09 ext file:  " + evtarray)
#2009 EXT Depth
ctr=ctr+1
if EVT_lines[ctr][:55]<>"20   1.00000(10e20.12)                  -1     ET DEPTH":
    print "Stopping: EVT file format change at 09 EXTD.  check:", cpath_py_upper+"/"+file_EVT
    exit()
HEADER=HEADER+'"EXTD09",'
iter_ct=0
for row in range(1,int(NROW)+1):
    curcol=0
    while curcol<(int(NCOL)):
        ctr=ctr+1
        dataline=EVT_lines[ctr]
        linevalues=dataline.split()
        for value in linevalues:
            curcol=curcol+1
            PROPS[iter_ct]=str(PROPS[iter_ct])+","+str(value)
            iter_ct=iter_ct+1
print("finished reading ET 09 Extinction Depth array from:  "+file_EVT)

#******************
#HDS
#******************
with open(cpath_py_upper+"/"+file_HDS, mode='rb') as file: ## b is important -> binary
    fileContent = file.read()
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
print ("calculating thickness, transmissivity 3-5-7, leak 2-4-6, drydepth, dtw, flooding...")
HEADER=HEADER[:-1]
calcslist=['th1', 'th2', 'th3', 'th4', 'th5', 'th6', 'th7', 'tr3', 'tr5', 'tr7', 'lk2', 'lk4', 'lk6',
           'drydep01','drydep09','dtw01','dtw09','fld01','fld09']
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
    kx1= float(vals[9])
    kx2= float(vals[10])
    kx3= float(vals[11])
    kx4= float(vals[12])
    kx5= float(vals[13])
    kx6= float(vals[14])
    kx7= float(vals[15])
    kz1= float(vals[16])
    kz2= float(vals[17])
    kz3= float(vals[18])
    kz4= float(vals[19])
    kz5= float(vals[20])
    kz6= float(vals[21])
    kz7= float(vals[22])
    ib1= float(vals[23])
    ib2= float(vals[24])
    ib3= float(vals[25])
    ib4= float(vals[26])
    ib5= float(vals[27])
    ib6= float(vals[28])
    ib7= float(vals[29])
    RCH01= float(vals[30])	
    RCH09= float(vals[31])
    ETSURF= float(vals[32])
    ETRATE01= float(vals[33])
    EXTD= float(vals[34])
    ETRATE09= float(vals[35])
    EXTD09= float(vals[36])
    HDS_L01SP1TS1= float(vals[37])
    HDS_L02SP1TS1= float(vals[38])
    HDS_L03SP1TS1= float(vals[39])
    HDS_L04SP1TS1= float(vals[40])
    HDS_L05SP1TS1= float(vals[41])
    HDS_L06SP1TS1= float(vals[42])
    HDS_L07SP1TS1= float(vals[43])
    HDS_L01SP2TS1= float(vals[44])
    HDS_L02SP2TS1= float(vals[45])
    HDS_L03SP2TS1= float(vals[46])
    HDS_L04SP2TS1= float(vals[47])
    HDS_L05SP2TS1= float(vals[48])
    HDS_L06SP2TS1= float(vals[49])
    HDS_L07SP2TS1= float(vals[50])

    #thickness calcs
    th1=float(L1Top)-float(L1Bot)
    th2=float(L1Bot)-float(L2Bot)
    th3=float(L2Bot)-float(L3Bot)
    th4=float(L3Bot)-float(L4Bot)
    th5=float(L4Bot)-float(L5Bot)
    th6=float(L5Bot)-float(L6Bot)
    th7=float(L6Bot)-float(L7Bot)
    #transmissivity calcs
    if th3<=0:
        tr3="0.00"
    else:
        tr3=float(kx3)*float(th3)
    if th5<=0:
        tr5="0.00"
    else:
        tr5=float(kx5)*float(th5)
    if th7<=0:
        tr7="0.00"
    else:
        tr7=float(kx7)*float(th7)
    #thickness calcs
    if th2<=0:
        lk2="0.00"
        #print(lk2)
        #break
    else:
        lk2=float(kz2)/float(th2)
    if th4<=0:
        lk4="0.00"
    else:
        lk4=float(kz4)/float(th4)
    if th6<=0:
        lk6="0.00"
    else:
        lk6=float(kz6)/float(th6)

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

    #'{0:02d}'.format(ILAY)
    PROPS[iter_ct]=str(PROPS[iter_ct])+","+str(th1)+","+str(th2)+","+str(th3)+","+str(th4)+","+str(th5)+","+str(th6)+","+str(th7)
    PROPS[iter_ct]=str(PROPS[iter_ct])+","+str(tr3)+","+str(tr5)+","+str(tr7)+","+str(lk2)+","+str(lk4)+","+str(lk6)
    PROPS[iter_ct]=str(PROPS[iter_ct])+","+str(drydep01)+","+str(drydep09)+","+str(dtw01)+","+str(dtw09)+","+str(fld01)+","+str(fld09)
    #th_calcs = str(th1)+","+str(th2)+","+str(th3)+","+str(th4)+","+str(th5)+","+str(th6)+","+str(th7)
    #propline=propline + "," + th_calcs
    #trlk_calcs = str(tr3)+","+str(tr5)+","+str(tr7)+","+str(lk2)+","+str(lk4)+","+str(lk6)
    #propline=propline + "," + trlk_calcs
    iter_ct=iter_ct+1
    #if iter_ct>10:
    #    print(tr3)
    #    print(PROPS[iter_ct])
    #    break

#output to a CSV table
iter_ct=0
with open(cpath_py+"/"+"ref.csv","w") as propscsv:
#        propscsv.write(item)
    propscsv.write(str(HEADER)+'\n')
    for line in PROPS:
        iter_ct=iter_ct+1
        propsline=line.split(",")
        #for i in propsline:
        #    print(i)
        #break
        propscsv.write('"'+str(propsline[0])+'"')
        for prop in range(1,len(propsline)):
            propscsv.write(","+str(propsline[prop]))
        propscsv.write('\n')
        #if iter_ct>10:
        #    print(tr3)
        #    print(PROPS[iter_ct])
        #    break
print("tmp csv output created")

arcpy.TableToTable_conversion(cpath_py+"/"+"ref.csv",gdb,"ref")
arcpy.MakeTableView_management(gdb+"/"+"ref","tbl_view")
arcpy.AddIndex_management("tbl_view","ROW_COL","ROW_COL","NON_UNIQUE","NON_ASCENDING")
print("tmp gdb table created")
#print("copying grid shape file")
#arcpy.Copy_management(nfseg_active_grid_poly,fpath+"/"+"temp.shp")
#print("done copying grid shape file")
arcpy.MakeFeatureLayer_management(nfseg_active_grid_poly,"shp_view")
#arcpy.AddField_management("shp_view","ROW_COL","TEXT","#","#","10","#","NULLABLE","NON_REQUIRED","#")
#rowcol_fields=['row','column','ROW_COL']
#with arcpy.da.UpdateCursor("shp_view",rowcol_fields) as cursor:
#    for row in cursor:
#        row[2]=str(row[0])+"_"+str(row[1])
#        cursor.updateRow(row)
#del cursor
#arcpy.AddIndex_management("shp_view","ROW_COL","#","NON_UNIQUE","NON_ASCENDING")
#print("done setting up grid shape file copy")

arcpy.AddJoin_management("shp_view","ROW_COL","tbl_view","ROW_COL","KEEP_ALL")
arcpy.FeatureClassToFeatureClass_conversion("shp_view",gdb,"nfseg_props")
arcpy.RemoveJoin_management("shp_view","#")

print("properties fc created")
print("cleaning up")
arcpy.Delete_management("shp_view")
arcpy.Delete_management("tbl_view")
arcpy.Delete_management(cpath_py+"/"+"ref.csv")

stop = time.clock()
DUR=round((stop-start)/60,1)
print("output: nfseg_props.shp in " + cpath_py )
print("completed in "+str(DUR)+" min")
