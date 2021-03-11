import arcpy
import sys
import os
import time
import numpy as np
arcpy.env.overwriteOutput = True
start = time.clock()

if arcpy.CheckExtension("Spatial") == "Available":
    arcpy.AddMessage("Checking out Spatial")
    arcpy.CheckOutExtension("Spatial")
else:
    arcpy.AddError("Unable to get spatial analyst extension-stopping")
    arcpy.AddMessage(arcpy.GetMessages(0))
    #sys.exit(0)
from arcpy.sa import *




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
else:
    print("props gdb:"+cpath_py+"/"+simnam+".gdb"+" was not found.  Script d1 must be run first.  Stopping")
    exit()

gdbZB=cpath_py+"/"+simnam+"_ZB.gdb"
if arcpy.Exists(gdbZB):
    print("geodatabase for this sim exists - continuing ")
else:
    print("ZB gdb:"+cpath_py+"/"+simnam+"_ZB.gdb"+" was not found.  Script a5 must be run first.  Stopping")
    exit()

#if os.path.isfile(cpath_py_upper+'/ref.csv') is False:
#    print "no props ref.csv file was found. Script a5 must be run first.  Stopping."
#else:
#    print "found props ref. ccsv file at: cpath_py_upper+'/ref.csv'"

###get number of rows and columns from the DIS file
file_DIS="nfseg.dis"
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
    print("number of colss: "+str(NCOL))

###basemap input (static)
base_gdb=cpath_py+"/templates/PEST_Baselayers.gdb"
nfseg_active_grid_poly=base_gdb+"/NFSEGActiveGrid_Albers_ROWCOL_LM"

###MAIN
arcpy.MakeFeatureLayer_management(nfseg_active_grid_poly,"grid_poly")

props_fc=gdb+'/nfseg_props'

#with the above 'loaded' into python it is fairly easy to create grids which allows for displaying
#non-MODFLOW units (e.g., rch in inches per year vs. ft/day, cbb fluxes, net recharge, etc.) but without
#creating cumbersome data files with redundancy

pivot_point = "22168.908 542244.152"
lowerleft = arcpy.Point(22168.908,542244.152)
arcpy.env.spatialGrid1 = 761.999963
cellsize=arcpy.env.spatialGrid1

#Assigned RCH01, RCH09, ETRATE01, ETRATE09 - (from nfseg_props) - EXD needs no units conversion, so fo str8 from polygon nfseg_props
RCH01 = np.empty([int(NROW),int(NCOL)])
RCH09 = np.empty([int(NROW),int(NCOL)])
ETRATE01 = np.empty([int(NROW),int(NCOL)])
ETRATE09 = np.empty([int(NROW),int(NCOL)])
for rval in range(0,int(NROW)):
    for cval in range(0,int(NCOL)):
        RCH01[rval,cval] = -9999999
        RCH09[rval,cval]  = -9999999
        ETRATE01[rval,cval]  = -9999999
        ETRATE09[rval,cval] = -9999999
with arcpy.da.SearchCursor(props_fc,["ref_ROW_COL","ref_RCH01","ref_RCH09","ref_ETRATE01","ref_ETRATE09","ref_IBND1"]) as cursor:
    for row in cursor:
        rowcol_items=row[0].split("_")
        rowval=int(rowcol_items[0])
        colval=int(rowcol_items[1])
        #print rowval,colval
        if row[5]==1:
            RCH01[rowval-1,colval-1]=float(row[1])*12*365 # convert ft/d to inches/year
            RCH09[rowval-1,colval-1]=float(row[2])*12*365 # convert ft/d to inches/year
            ETRATE01[rowval-1,colval-1]=float(row[3])*12*365 # convert ft/d to inches/year
            ETRATE09[rowval-1,colval-1]=float(row[4])*12*365 # convert ft/d to inches/year
        #else:
            #RCH01[rowval-1,colval-1]=np.NaN# blank
            #RCH09[rowval-1,colval-1]=np.NaN# blank
            #ETRATE01[rowval-1,colval-1]=np.NaN# blank
            #ETRATE09[rowval-1,colval-1]=np.NaN# blank
RCH01_filt = np.where(RCH01== -9999999,np.NaN,RCH01)
RCH09_filt = np.where(RCH09== -9999999,np.NaN,RCH09)
ETRATE01_filt = np.where(ETRATE01== -9999999,np.NaN,ETRATE01)
ETRATE09_filt = np.where(ETRATE09== -9999999,np.NaN,ETRATE09)
ras = arcpy.NumPyArrayToRaster(RCH01_filt,lowerleft,cellsize,cellsize,9999)
rasrot = arcpy.Rotate_management(ras, gdb+"/RCH01_INYR", "-25",pivot_point)
ras = arcpy.NumPyArrayToRaster(RCH09_filt,lowerleft,cellsize,cellsize,9999)
rasrot = arcpy.Rotate_management(ras, gdb+"/RCH09_INYR", "-25",pivot_point)
ras = arcpy.NumPyArrayToRaster(ETRATE01_filt,lowerleft,cellsize,cellsize,9999)
rasrot = arcpy.Rotate_management(ras, gdb+"/ETRATE01_INYR", "-25",pivot_point)
ras = arcpy.NumPyArrayToRaster(ETRATE09_filt,lowerleft,cellsize,cellsize,9999)
rasrot = arcpy.Rotate_management(ras, gdb+"/ETRATE09_INYR", "-25",pivot_point)
#THE ABOVE CREATES SIMPLE RASTERS and CONTOURS quickly, below is needed to reproduce the detailed
#symbology (polygons with different outline colors).  create a poly fc now
arcpy.CreateFeatureclass_management(gdb,"nfseg_props_ETRCHinp","POLYGON",nfseg_active_grid_poly)
arcpy.AddField_management(gdb+"/nfseg_props_ETRCHinp","RCH01_INYR","DOUBLE")
arcpy.AddField_management(gdb+"/nfseg_props_ETRCHinp","RCH09_INYR","DOUBLE")
arcpy.AddField_management(gdb+"/nfseg_props_ETRCHinp","ETRATE01_INYR","DOUBLE")
arcpy.AddField_management(gdb+"/nfseg_props_ETRCHinp","ETRATE09_INYR","DOUBLE")
with arcpy.da.InsertCursor(gdb+"/nfseg_props_ETRCHinp",["Shape@","ROW_COL","row","column_",
                                                        "RCH01_INYR","RCH09_INYR",
                                                        "ETRATE01_INYR","ETRATE09_INYR"]) as inscursor:
    with arcpy.da.SearchCursor(props_fc,["Shape@","ref_ROW_COL"]) as cursor:
        for row in cursor:
            insrow=[]
            insrow.append(row[0])
            insrow.append(row[1])
            rowcol_items=row[1].split("_")
            rowval=int(rowcol_items[0])
            colval=int(rowcol_items[1])
            insrow.append(rowval)
            insrow.append(colval)
            insrow.append(RCH01_filt[rowval-1,colval-1])
            insrow.append(RCH09_filt[rowval-1,colval-1])
            insrow.append(ETRATE01_filt[rowval-1,colval-1])
            insrow.append(ETRATE09_filt[rowval-1,colval-1])
            inscursor.insertRow(insrow)

#HDS for L1 in both 2001 and 2009 --> ultimately want contours for each at both 5 and 50-ft intervals
for hdsfld in ["ref_HDS_L01SP1TS1","ref_HDS_L01SP2TS1"]:
    HDSRAS = np.empty([int(NROW),int(NCOL)])
    for rval in range(0,int(NROW)):
        for cval in range(0,int(NCOL)):
            HDSRAS[rval,cval] = -9999999
    with arcpy.da.SearchCursor(props_fc,["ref_ROW_COL",hdsfld,"ref_IBND1"]) as cursor:
        for row in cursor:
            rowcol_items=row[0].split("_")
            rowval=int(rowcol_items[0])
            colval=int(rowcol_items[1])
            #print rowval,colval
            if row[2]==1:
                HDSRAS[rowval-1,colval-1]=float(row[1])# no conversion
            else:
                HDSRAS[rowval-1,colval-1]=-9999999
    HDSRAS_filt = np.where(HDSRAS== -9999999,np.NaN,HDSRAS)
    ras = arcpy.NumPyArrayToRaster(HDSRAS_filt,lowerleft,cellsize,cellsize,9999)
    rasrot = arcpy.Rotate_management(ras, gdb+"/"+hdsfld, "-25",pivot_point) 
    arcpy.sa.Contour(gdb+"/"+hdsfld,gdb+"/"+hdsfld+"_cont50ft","50","0")
    arcpy.sa.Contour(gdb+"/"+hdsfld,gdb+"/"+hdsfld+"_cont5ft","5","0")
#HDS for L3 in both 2001 and 2009 --> ultimately want contours for each at both 5 and 50-ft intervals
for hdsfld in ["ref_HDS_L03SP1TS1","ref_HDS_L03SP2TS1"]:
    HDSRAS = np.empty([int(NROW),int(NCOL)])
    for rval in range(0,int(NROW)):
        for cval in range(0,int(NCOL)):
            HDSRAS[rval,cval] = -9999999
    with arcpy.da.SearchCursor(props_fc,["ref_ROW_COL",hdsfld,"ref_IBND3"]) as cursor:
        for row in cursor:
            rowcol_items=row[0].split("_")
            rowval=int(rowcol_items[0])
            colval=int(rowcol_items[1])
            #print rowval,colval
            if row[2]==1:
                HDSRAS[rowval-1,colval-1]=float(row[1])# no conversion
            else:
                HDSRAS[rowval-1,colval-1]=-9999999
    HDSRAS_filt = np.where(HDSRAS== -9999999,np.NaN,HDSRAS)
    ras = arcpy.NumPyArrayToRaster(HDSRAS_filt,lowerleft,cellsize,cellsize,9999)
    rasrot = arcpy.Rotate_management(ras, gdb+"/"+hdsfld, "-25",pivot_point)
    arcpy.sa.Contour(gdb+"/"+hdsfld,gdb+"/"+hdsfld+"_cont50ft","50","0")
    arcpy.sa.Contour(gdb+"/"+hdsfld,gdb+"/"+hdsfld+"_cont5ft","5","0")
#HDS for L5 in both 2001 and 2009 --> ultimately want contours for each at both 5 and 50-ft intervals
for hdsfld in ["ref_HDS_L05SP1TS1","ref_HDS_L05SP2TS1"]:
    HDSRAS = np.empty([int(NROW),int(NCOL)])
    for rval in range(0,int(NROW)):
        for cval in range(0,int(NCOL)):
            HDSRAS[rval,cval] = -9999999
    with arcpy.da.SearchCursor(props_fc,["ref_ROW_COL",hdsfld,"ref_IBND5"]) as cursor:
        for row in cursor:
            rowcol_items=row[0].split("_")
            rowval=int(rowcol_items[0])
            colval=int(rowcol_items[1])
            #print rowval,colval
            if row[2]==1:
                HDSRAS[rowval-1,colval-1]=float(row[1])# no conversion
            else:
                HDSRAS[rowval-1,colval-1]=-9999999
    HDSRAS_filt = np.where(HDSRAS== -9999999,np.NaN,HDSRAS)
    ras = arcpy.NumPyArrayToRaster(HDSRAS_filt,lowerleft,cellsize,cellsize,9999)
    rasrot = arcpy.Rotate_management(ras, gdb+"/"+hdsfld, "-25",pivot_point)
    arcpy.sa.Contour(gdb+"/"+hdsfld,gdb+"/"+hdsfld+"_cont50ft","50","0")
    arcpy.sa.Contour(gdb+"/"+hdsfld,gdb+"/"+hdsfld+"_cont5ft","5","0")

#SIMULATED NET RECHARGE, Vertical flow L2-to-L3, L2-to-L1, L4-to-L3, L4-to-L5 for both 01 and 09
for YEARVAL in ['2001','2009']:
    YY=YEARVAL[-2:]
    cbb_fc = gdbZB+'/nfseg_all_to_cbc_cbc_'+str(YEARVAL)+'_csv'
    if arcpy.Exists(cbb_fc) is False:
        print "stopping - cbb_fc not found: "+cbb_fc
        exit()
    CBB_LOWERFACE = np.empty([int(NLAY),int(NROW),int(NCOL)])
    NETRCH = np.empty([int(NROW),int(NCOL)])
    for lval in range(0,int(NLAY)):
        for rval in range(0,int(NROW)):
            for cval in range(0,int(NCOL)):
                CBB_LOWERFACE[lval,rval,cval] = -9999999
                if lval==0:
                    NETRCH[rval,cval] = -9999999
    with arcpy.da.SearchCursor(cbb_fc,["ROW_COL","LAY","FLOW_LOWER_FACE","RECHARGE","ET"]) as cursor:
        for row in cursor:
            rowcol_items=row[0].split("_")
            rowval=int(rowcol_items[0])
            colval=int(rowcol_items[1])
            layval=int(row[1])-1
            CBB_LOWERFACE[layval-1,rowval-1,colval-1] = float(row[2])/(2500*2500)*12*365 # converts cfd to in/yr over cell area
            if NETRCH[rowval-1,colval-1]== -9999999:
                NETRCH[rowval-1,colval-1]=(float(row[3])+float(row[4]))/(2500*2500)*12*365 # ET is included as a negative number in the cbb csv file
            else:
                NETRCH[rowval-1,colval-1]=NETRCH[rowval-1,colval-1]+(float(row[3])+float(row[4]))/(2500*2500)*12*365 # add to the prev layer, should be all zero but might not for other simulations

    NETRCH_filt = np.where(NETRCH== -9999999,np.NaN,NETRCH)
    CBB_LOWERFACE_filt = np.where(CBB_LOWERFACE== -9999999,np.NaN,CBB_LOWERFACE)
    for lval in range(0,int(NLAY)):
        ras = arcpy.NumPyArrayToRaster(CBB_LOWERFACE_filt[lval,:,:],lowerleft,cellsize,cellsize,9999)
        rasrot = arcpy.Rotate_management(ras, gdbZB+"/CBB_LOWER_L"+str(lval+1)+"_INYR_"+YY, "-25",pivot_point)
    ras = arcpy.NumPyArrayToRaster(NETRCH_filt,lowerleft,cellsize,cellsize,9999)
    rasrot = arcpy.Rotate_management(ras, gdbZB+"/CBB_NETRCH_INYR_"+YY, "-25",pivot_point)
    print("finished with:"+cbb_fc)

    #THE ABOVE CREATES SIMPLE RASTERS and CONTOURS quickly, below is needed to reproduce the detailed
    #symbology (polygons with different outline colors).  create a poly fc now
    #CBB_LOWERFACE for Layer 2 and Layer 4
    arcpy.CreateFeatureclass_management(gdbZB,"cbb_props_calcs"+str(YY),"POLYGON",nfseg_active_grid_poly)
    arcpy.AddField_management(gdbZB+"/cbb_props_calcs"+str(YY),"NTRCH"+str(YY)+"_INYR","DOUBLE")
    arcpy.AddField_management(gdbZB+"/cbb_props_calcs"+str(YY),"QLF_L2_"+str(YY)+"_INYR","DOUBLE")
    arcpy.AddField_management(gdbZB+"/cbb_props_calcs"+str(YY),"QLF_L4_"+str(YY)+"_INYR","DOUBLE")
    with arcpy.da.InsertCursor(gdbZB+"/cbb_props_calcs"+str(YY),["Shape@","ROW_COL","row","column_",
                                                            "NTRCH"+str(YY)+"_INYR",
                                                            "QLF_L2_"+str(YY)+"_INYR",
                                                            "QLF_L4_"+str(YY)+"_INYR"]) as inscursor:
        with arcpy.da.SearchCursor(props_fc,["Shape@","ref_ROW_COL"]) as cursor:
            for row in cursor:
                insrow=[]
                insrow.append(row[0])
                insrow.append(row[1])
                rowcol_items=row[1].split("_")
                rowval=int(rowcol_items[0])
                colval=int(rowcol_items[1])
                insrow.append(rowval)
                insrow.append(colval)
                insrow.append(NETRCH_filt[rowval-1,colval-1])
                insrow.append(CBB_LOWERFACE_filt[1,rowval-1,colval-1]) # note 0 is layer 1 in 3d numpy array
                insrow.append(CBB_LOWERFACE_filt[3,rowval-1,colval-1])
                inscursor.insertRow(insrow)
