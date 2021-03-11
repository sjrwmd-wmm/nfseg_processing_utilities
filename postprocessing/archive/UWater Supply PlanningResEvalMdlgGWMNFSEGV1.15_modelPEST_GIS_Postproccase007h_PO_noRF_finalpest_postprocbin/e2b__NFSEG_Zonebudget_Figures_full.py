import arcpy
import sys
import os
import time
arcpy.env.overwriteOutput = True
start = time.clock()
import numpy as np
import fnmatch

start = time.clock()

# routines to flip arrows (trd 20171201)
def flipUP(elename):
    for gre in greList:
        if gre.name == (ele.name+"_arrow"):
            XPOS = gre.elementPositionX
            YPOS = gre.elementPositionY
            gre.delete()
            NEWARROW = UPARROW.clone("_clone")
            NEWARROW.elementPositionX=XPOS
            NEWARROW.elementPositionY=YPOS
            NEWARROW.name=gre.name
def flipDOWN(elename):
    for gre in greList:
        if gre.name == (ele.name+"_arrow"):
            XPOS = gre.elementPositionX
            YPOS = gre.elementPositionY
            gre.delete()
            NEWARROW = DOWNARROW.clone("_clone")
            NEWARROW.elementPositionX=XPOS
            NEWARROW.elementPositionY=YPOS
            NEWARROW.name=gre.name
def flipLEFT(elename):
    for gre in greList:
        if gre.name == (ele.name+"_arrow"):
            XPOS = gre.elementPositionX
            YPOS = gre.elementPositionY
            gre.delete()
            NEWARROW = LEFTARROW.clone("_clone")
            NEWARROW.elementPositionX=XPOS
            NEWARROW.elementPositionY=YPOS
            NEWARROW.name=gre.name
def flipRIGHT(elename):
    for gre in greList:
        if gre.name == (ele.name+"_arrow"):
            XPOS = gre.elementPositionX
            YPOS = gre.elementPositionY
            gre.delete()
            NEWARROW = RIGHTARROW.clone("_clone")
            NEWARROW.elementPositionX=XPOS
            NEWARROW.elementPositionY=YPOS
            NEWARROW.name=gre.name

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
    #arcpy.CreateFileGDB_management(cpath_py,simnam+"_ZB","9.3")
    print("geodatabase for this sim does not exist - stopping - run s9 cbb_fc first at least")

###check for a sub directory called /ZB, create it if necessary
dir_ZB=str(cpath_py)+"/ZB"
if os.path.exists(dir_ZB) == False:
    os.makedirs(dir_ZB)
else:
    print("subdirectory / ZB directory already exists - existing files will be overwritten without any further warning")
print("root directory for ZB output: "+str(dir_ZB))

###basemap input (static)
base_gdb=cpath_py+"/templates/PEST_Baselayers.gdb"
MassBal_poly=base_gdb+"/nfseg_zonebudget_polygons"

###Setup graphics_fieldnames (onetime)
laylist=["L01_","L02_","L03_","L04_","L05_","L06_","L07_"]
graphics_fieldnames=["ZB_NAME","NUMCELLS"] # positions 0 to 1
for layer_prefix in laylist:
    graphics_fieldnames.append(str(layer_prefix)+'FLOW_LATERAL_NET') # LATERAL FLOWS; positions 2 to 8
for layer_prefix in laylist:
    graphics_fieldnames.append(str(layer_prefix)+'FLOW_LOWER_FACE') # DOWNWARD FLOW; positions 9 to 15
for layer_prefix in laylist:
    graphics_fieldnames.append(str(layer_prefix)+'RECHARGE') # RECHARGES; positions 16 to 22
for layer_prefix in laylist:
    graphics_fieldnames.append(str(layer_prefix)+'ET') # ET; positions 23 to 29
for layer_prefix in laylist:
    graphics_fieldnames.append(str(layer_prefix)+'WELLS') # WELLS; positions 30 to 36
graphics_fieldnames.append('L01_DRAINS') # L1 DRAINS; position 37
graphics_fieldnames.append('L01_RIVER_LEAKAGE') # L1 RIVS(springs); position 38
graphics_fieldnames.append('L02_RIVER_LEAKAGE') # L2 RIVS (springs); position 39
graphics_fieldnames.append('L03_RIVER_LEAKAGE') # L3 RIVS (springs); position 40
for layer_prefix in laylist:
    graphics_fieldnames.append(str(layer_prefix)+'HEAD_DEP_BOUNDS') # GHBs; positions 41 to 47
graphics_fieldnames.append('L01_CONSTANT_HEAD') # L1 CH (springs); position 48
#print graphics_fieldnames
for layer_prefix in laylist:
    graphics_fieldnames.append(str(layer_prefix)+'MNW2') # MNW2 wells; positions 49 to 55

YEARS=['2001','2009']
for yearval2 in YEARS:
    print yearval2
    cbb_poly_fc=gdb+'/'+simnam+'_'+str(yearval2)+'_cbb_poly'
    with arcpy.da.SearchCursor(cbb_poly_fc,graphics_fieldnames) as SRC2cursor:
        for row3 in SRC2cursor:

            #for each figure, we need to re-read the template mxd to make sure the sign changes don't get mismatched...
            template_mxd = arcpy.mapping.MapDocument(cpath_py+"/templates/nfseg_zonebudget_full.mxd")
            #template_mxd = arcpy.mapping.MapDocument("CURRENT") # dfor debugging in arcmpa
            lyrList = arcpy.mapping.ListLayers(template_mxd)
            eleList = arcpy.mapping.ListLayoutElements(template_mxd, "TEXT_ELEMENT")
            greList = arcpy.mapping.ListLayoutElements(template_mxd,"GRAPHIC_ELEMENT")
            ###update the figures
            for lyr in lyrList:
                if lyr.name=='nfseg_zonebudget_polygons':
                    arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",simnam+'_'+str(yearval2)+'_cbb_poly')
            # assign variables to the flip arrows set outside of the page
            for gre in greList:
                if gre.name == "UPARROW":
                    UPARROW = gre
                if gre.name == "DOWNARROW":
                    DOWNARROW = gre
                if gre.name == "LEFTARROW":
                    LEFTARROW = gre
                if gre.name == "RIGHTARROW":
                    RIGHTARROW = gre


            ZB_NAME=row3[0]
            print(ZB_NAME)
            CELLAREA_SQFT=row3[1]*2500*2500
            L1_Q_LAT__inyr=row3[2]/CELLAREA_SQFT*12*365*-1
            L2_Q_LAT__inyr=row3[3]/CELLAREA_SQFT*12*365*-1
            L3_Q_LAT__inyr=row3[4]/CELLAREA_SQFT*12*365*-1
            L4_Q_LAT__inyr=row3[5]/CELLAREA_SQFT*12*365*-1
            L5_Q_LAT__inyr=row3[6]/CELLAREA_SQFT*12*365*-1
            L6_Q_LAT__inyr=row3[7]/CELLAREA_SQFT*12*365*-1
            L7_Q_LAT__inyr=row3[8]/CELLAREA_SQFT*12*365*-1
            #L567_Q_LAT__inyr=(row3[6]+row3[7]+row3[8])/CELLAREA_SQFT*12*365*-1

            L1_Q_LOWER__inyr=row3[9]/CELLAREA_SQFT*12*365
            L2_Q_LOWER__inyr=row3[10]/CELLAREA_SQFT*12*365
            L3_Q_LOWER__inyr=row3[11]/CELLAREA_SQFT*12*365
            L4_Q_LOWER__inyr=row3[12]/CELLAREA_SQFT*12*365
            L5_Q_LOWER__inyr=row3[13]/CELLAREA_SQFT*12*365
            L6_Q_LOWER__inyr=row3[14]/CELLAREA_SQFT*12*365

            RCH_ALL__inyr=(row3[16]+row3[17]+row3[18]+row3[19]+row3[20]+row3[21]+row3[22])/CELLAREA_SQFT*12*365
            ET_ALL__inyr=(row3[23]+row3[24]+row3[25]+row3[26]+row3[27]+row3[28]+row3[29])/CELLAREA_SQFT*12*365*-1

            L1_Q_WEL__inyr=(row3[30]+row3[49])/CELLAREA_SQFT*12*365*-1 #adds regular WEL and MNW2 wells
            L2_Q_WEL__inyr=(row3[31]+row3[50])/CELLAREA_SQFT*12*365*-1 #adds regular WEL and MNW2 wells
            L3_Q_WEL__inyr=(row3[32]+row3[51])/CELLAREA_SQFT*12*365*-1 #adds regular WEL and MNW2 wells
            L4_Q_WEL__inyr=(row3[33]+row3[52])/CELLAREA_SQFT*12*365*-1 #adds regular WEL and MNW2 wells
            L5_Q_WEL__inyr=(row3[34]+row3[53])/CELLAREA_SQFT*12*365*-1 #adds regular WEL and MNW2 wells
            L6_Q_WEL__inyr=(row3[35]+row3[54])/CELLAREA_SQFT*12*365*-1 #adds regular WEL and MNW2 wells
            L7_Q_WEL__inyr=(row3[36]+row3[55])/CELLAREA_SQFT*12*365*-1 #adds regular WEL and MNW2 wells
            #L567_Q_WEL__inyr=(row3[34]+row3[53]+row3[35]+row3[54]+row3[36]+row3[55])/CELLAREA_SQFT*12*365*-1

            L1_Q_DRN__inyr=row3[37]/CELLAREA_SQFT*12*365*-1

            L1_Q_RIV__inyr=row3[38]/CELLAREA_SQFT*12*365*-1
            L2_Q_RIV__inyr=row3[39]/CELLAREA_SQFT*12*365*-1
            L3_Q_RIV__inyr=row3[40]/CELLAREA_SQFT*12*365*-1

            L1_Q_GHB__inyr=row3[41]/CELLAREA_SQFT*12*365*-1
            L2_Q_GHB__inyr=row3[42]/CELLAREA_SQFT*12*365*-1
            L3_Q_GHB__inyr=row3[43]/CELLAREA_SQFT*12*365*-1
            L4_Q_GHB__inyr=row3[44]/CELLAREA_SQFT*12*365*-1
            L5_Q_GHB__inyr=row3[45]/CELLAREA_SQFT*12*365*-1
            L6_Q_GHB__inyr=row3[46]/CELLAREA_SQFT*12*365*-1
            L7_Q_GHB__inyr=row3[47]/CELLAREA_SQFT*12*365*-1
            #L567_Q_GHB__inyr=(row3[45]+row3[46]+row3[47])/CELLAREA_SQFT*12*365*-1

            L1_Q_CH__inyr=row3[48]/CELLAREA_SQFT*12*365*-1

            for ele in eleList:
                #Qlat, default points to the right
                if ele.name == "L1 Q_LAT":
                    ele.text="L1 Q_LAT: "+str('{:5.2f}'.format(abs(L1_Q_LAT__inyr))) 
                    if (L1_Q_LAT__inyr+L1_Q_GHB__inyr)<0:
                        ele.text="L1 Q_LAT: "+str('{:5.2f}'.format(abs((L1_Q_LAT__inyr)))) 
                        flipLEFT(ele.name)
                if ele.name == "L2 Q_LAT":
                    ele.text="L2 Q_LAT: "+str('{:5.2f}'.format(abs(L2_Q_LAT__inyr))) 
                    if (L2_Q_LAT__inyr+L2_Q_GHB__inyr)<0:
                        ele.text="L2 Q_LAT: "+str('{:5.2f}'.format(abs((L2_Q_LAT__inyr)))) 
                        flipLEFT(ele.name)
                if ele.name == "L3 Q_LAT":
                    ele.text="L3 Q_LAT: "+str('{:5.2f}'.format(abs(L3_Q_LAT__inyr)))  
                    if (L3_Q_LAT__inyr)<=0:
                        ele.text="L3 Q_LAT: "+str('{:5.2f}'.format(abs((L3_Q_LAT__inyr)))) 
                        flipLEFT(ele.name)
                if ele.name == "L4 Q_LAT":
                    ele.text="L4 Q_LAT: "+str('{:5.2f}'.format(abs(L4_Q_LAT__inyr))) 
                    if (L4_Q_LAT__inyr+L4_Q_GHB__inyr)<0:
                        ele.text="L4 Q_LAT: "+str('{:5.2f}'.format(abs((L4_Q_LAT__inyr)))) 
                        flipLEFT(ele.name)
                if ele.name == "L5 Q_LAT":
                    ele.text="L5 Q_LAT: "+str('{:5.2f}'.format(abs(L5_Q_LAT__inyr))) 
                    if (L5_Q_LAT__inyr+L5_Q_GHB__inyr)<0:
                        ele.text="L5 Q_LAT: "+str('{:5.2f}'.format(abs((L5_Q_LAT__inyr)))) 
                        flipLEFT(ele.name)
                if ele.name == "L6 Q_LAT":
                    ele.text="L6 Q_LAT: "+str('{:5.2f}'.format(abs(L6_Q_LAT__inyr))) 
                    if (L6_Q_LAT__inyr+L6_Q_GHB__inyr)<0:
                        ele.text="L6 Q_LAT: "+str('{:5.2f}'.format(abs((L6_Q_LAT__inyr)))) 
                        flipLEFT(ele.name)
                if ele.name == "L7 Q_LAT":
                    ele.text="L7 Q_LAT: "+str('{:5.2f}'.format(abs(L7_Q_LAT__inyr))) 
                    if (L7_Q_LAT__inyr+L7_Q_GHB__inyr)<0:
                        ele.text="L7 Q_LAT: "+str('{:5.2f}'.format(abs((L7_Q_LAT__inyr)))) 
                        flipLEFT(ele.name)
                # vertical flow terms, default arrow is downward
                if ele.name == "L1_Q_LOWER":
                    ele.text="L1 to L2: "+str('{:5.2f}'.format(abs(L1_Q_LOWER__inyr)))
                    if L1_Q_LOWER__inyr<0:
                        ele.text="L2 to L1: "+str('{:5.2f}'.format(abs(L1_Q_LOWER__inyr)))
                        flipUP(ele.name)
                if ele.name == "L2_Q_LOWER":
                    ele.text="L2 to L3: "+str('{:5.2f}'.format(abs(L2_Q_LOWER__inyr)))
                    if L2_Q_LOWER__inyr<0:
                        ele.text="L3 to L2: "+str('{:5.2f}'.format(abs(L2_Q_LOWER__inyr)))
                        flipUP(ele.name)
                if ele.name == "L3_Q_LOWER":
                    ele.text="L3 to L4: "+str('{:5.2f}'.format(abs(L3_Q_LOWER__inyr)))
                    if L3_Q_LOWER__inyr<0:
                        ele.text="L4 to L3: "+str('{:5.2f}'.format(abs(L3_Q_LOWER__inyr)))
                        flipUP(ele.name)
                if ele.name == "L4_Q_LOWER":
                    ele.text="L4 to L5: "+str('{:5.2f}'.format(abs(L4_Q_LOWER__inyr)))
                    if L4_Q_LOWER__inyr<0:
                        ele.text="L5 to L4: "+str('{:5.2f}'.format(abs(L4_Q_LOWER__inyr)))
                        flipUP(ele.name)
                if ele.name == "L5_Q_LOWER":
                    ele.text="L5 to L6: "+str('{:5.2f}'.format(abs(L5_Q_LOWER__inyr)))
                    if L5_Q_LOWER__inyr<0:
                        ele.text="L5 to L6: "+str('{:5.2f}'.format(abs(L5_Q_LOWER__inyr)))
                        flipUP(ele.name)
                if ele.name == "L6_Q_LOWER":
                    ele.text="L6 to L7: "+str('{:5.2f}'.format(abs(L6_Q_LOWER__inyr)))
                    if L6_Q_LOWER__inyr<0:
                        ele.text="L6 to L7: "+str('{:5.2f}'.format(abs(L6_Q_LOWER__inyr)))
                        flipUP(ele.name)

                #recharge, default down
                if ele.name == "RCH":
                    ele.text="RCH: "+str('{:5.2f}'.format(abs(RCH_ALL__inyr)))
                    if RCH_ALL__inyr<0:
                        ele.text="RCH: "+str('{:5.2f}'.format(abs(RCH_ALL__inyr)))
                        flipUP(ele.name)
                #GW ET, default up should always be positive but just in case...
                if ele.name == "GW ET":
                    ele.text="GW ET: "+str('{:5.2f}'.format(abs(ET_ALL__inyr)))
                    if ET_ALL__inyr<0:
                        ele.text="GW ET: "+str('{:5.2f}'.format(abs(ET_ALL__inyr)))
                        flipDOWN(ele.name)

                #WEL, default is to the right
                if ele.name == "L1 Q_WEL":
                    ele.text="L1 Q_WEL: "+str('{:5.2f}'.format(abs(L1_Q_WEL__inyr)))
                    if (L1_Q_WEL__inyr)<0:
                        ele.text="L1 Q_WEL: "+str('{:5.2f}'.format(abs(L1_Q_WEL__inyr))) # plus L1 GHB here...
                        flipLEFT(ele.name)
                if ele.name == "L2 Q_WEL":
                    ele.text="L2 Q_WEL: "+str('{:5.2f}'.format(abs(L2_Q_WEL__inyr)))
                    if (L2_Q_WEL__inyr)<0:
                        ele.text="L2 Q_WEL: "+str('{:5.2f}'.format(abs(L2_Q_WEL__inyr))) # plus L1 GHB here...
                        flipLEFT(ele.name)
                if ele.name == "L3 Q_WEL":
                    ele.text="L3 Q_WEL: "+str('{:5.2f}'.format(abs(L3_Q_WEL__inyr)))
                    if (L3_Q_WEL__inyr)<0:
                        ele.text="L3 Q_WEL: "+str('{:5.2f}'.format(abs(L3_Q_WEL__inyr))) # plus L1 GHB here...
                        flipLEFT(ele.name)
                if ele.name == "L4 Q_WEL":
                    ele.text="L4 Q_WEL: "+str('{:5.2f}'.format(abs(L4_Q_WEL__inyr)))
                    if (L4_Q_WEL__inyr)<0:
                        ele.text="L4 Q_WEL: "+str('{:5.2f}'.format(abs(L4_Q_WEL__inyr))) # plus L1 GHB here...
                        flipLEFT(ele.name)
                if ele.name == "L5 Q_WEL":
                    ele.text="L5 Q_WEL: "+str('{:5.2f}'.format(abs(L5_Q_WEL__inyr)))
                    if (L5_Q_WEL__inyr)<0:
                        ele.text="L5 Q_WEL: "+str('{:5.2f}'.format(abs(L5_Q_WEL__inyr))) # plus L1 GHB here...
                        flipLEFT(ele.name)
                if ele.name == "L6 Q_WEL":
                    ele.text="L6 Q_WEL: "+str('{:5.2f}'.format(abs(L6_Q_WEL__inyr)))
                    if (L6_Q_WEL__inyr)<0:
                        ele.text="L6 Q_WEL: "+str('{:5.2f}'.format(abs(L6_Q_WEL__inyr))) # plus L1 GHB here...
                        flipLEFT(ele.name)
                if ele.name == "L7 Q_WEL":
                    ele.text="L7 Q_WEL: "+str('{:5.2f}'.format(abs(L7_Q_WEL__inyr)))
                    if (L7_Q_WEL__inyr)<0:
                        ele.text="L7 Q_WEL: "+str('{:5.2f}'.format(abs(L7_Q_WEL__inyr))) # plus L1 GHB here...
                        flipLEFT(ele.name)
                #well flows in mgd
                if ele.name == "L1_WEL_mgd":
                    mgdval=L1_Q_WEL__inyr/12*CELLAREA_SQFT/365*7.4805/1000000
                    mgdval=abs(mgdval)
                    ele.text="(L1 Q_WEL: "+str('{:5.2f}'.format(mgdval))+ " mgd)"
                if ele.name == "L2_WEL_mgd":
                    mgdval=L2_Q_WEL__inyr/12*CELLAREA_SQFT/365*7.4805/1000000
                    mgdval=abs(mgdval)
                    ele.text="(L2 Q_WEL: "+str('{:5.2f}'.format(mgdval))+ " mgd)"
                if ele.name == "L3_WEL_mgd":
                    mgdval=L3_Q_WEL__inyr/12*CELLAREA_SQFT/365*7.4805/1000000
                    mgdval=abs(mgdval)
                    ele.text="(L3 Q_WEL: "+str('{:5.2f}'.format(mgdval))+ " mgd)"
                if ele.name == "L4_WEL_mgd":
                    mgdval=L4_Q_WEL__inyr/12*CELLAREA_SQFT/365*7.4805/1000000
                    mgdval=abs(mgdval)
                    ele.text="(L4 Q_WEL: "+str('{:5.2f}'.format(mgdval))+ " mgd)"
                if ele.name == "L5_WEL_mgd":
                    mgdval=L5_Q_WEL__inyr/12*CELLAREA_SQFT/365*7.4805/1000000
                    mgdval=abs(mgdval)
                    ele.text="(L5 Q_WEL: "+str('{:5.2f}'.format(mgdval))+ " mgd)"
                if ele.name == "L6_WEL_mgd":
                    mgdval=L6_Q_WEL__inyr/12*CELLAREA_SQFT/365*7.4805/1000000
                    mgdval=abs(mgdval)
                    ele.text="(L6 Q_WEL: "+str('{:5.2f}'.format(mgdval))+ " mgd)"
                if ele.name == "L7_WEL_mgd":
                    mgdval=L7_Q_WEL__inyr/12*CELLAREA_SQFT/365*7.4805/1000000
                    mgdval=abs(mgdval)
                    ele.text="(L7 Q_WEL: "+str('{:5.2f}'.format(mgdval))+ " mgd)"

                #L1 BCs
                if ele.name == "L1 CH":
                    ele.text="L1 CH: "+str('{:5.2f}'.format(abs(L1_Q_CH__inyr)))
                    if (L1_Q_CH__inyr)<0:
                        ele.text="L1 CH: "+str('{:5.2f}'.format(abs(L1_Q_CH__inyr))) 
                        flipRIGHT(ele.name)
                if ele.name == "L1 DRN":
                    ele.text="L1 DRN: "+str('{:5.2f}'.format(abs(L1_Q_DRN__inyr)))
                    if (L1_Q_DRN__inyr)<0:
                        ele.text="L1 DRN: "+str('{:5.2f}'.format(abs(L1_Q_DRN__inyr))) 
                        flipRIGHT(ele.name)
                if ele.name == "L1 RIV":
                    ele.text="L1 RIV: "+str('{:5.2f}'.format(abs(L1_Q_RIV__inyr)))
                    if (L1_Q_RIV__inyr)<0:
                        ele.text="L1 RIV: "+str('{:5.2f}'.format(abs(L1_Q_RIV__inyr))) 
                        flipRIGHT(ele.name)
                #L2 BCs
                if ele.name == "L2 GHB":
                    ele.text="L2 GHB: "+str('{:5.2f}'.format(abs(L2_Q_GHB__inyr)))  # keep separate
                    if (L2_Q_GHB__inyr)<0:
                        ele.text="L2 GHB: "+str('{:5.2f}'.format(abs(L2_Q_GHB__inyr))) 
                        flipRIGHT(ele.name)
                if ele.name == "L2 RIV":
                    ele.text="L2 RIV: "+str('{:5.2f}'.format(abs(L2_Q_RIV__inyr)))
                    if (L2_Q_RIV__inyr)<0:
                        ele.text="L2 RIV: "+str('{:5.2f}'.format(abs(L2_Q_RIV__inyr))) 
                        flipRIGHT(ele.name)
                #L3 BCs
                if ele.name == "L3 RIV":
                    ele.text="L3 RIV: "+str('{:5.2f}'.format(abs(L3_Q_RIV__inyr)))
                    if (L3_Q_RIV__inyr)<0:
                        ele.text="L3 RIV: "+str('{:5.2f}'.format(abs(L3_Q_RIV__inyr))) 
                        flipRIGHT(ele.name)
                if ele.name == "L3 GHB":
                    ele.text="L3 GHB: "+str('{:5.2f}'.format(abs(L3_Q_GHB__inyr)))
                    if (L3_Q_GHB__inyr)<0:
                        ele.text="L3 GHB: "+str('{:5.2f}'.format(abs(L3_Q_GHB__inyr))) 
                        flipRIGHT(ele.name)
                #L4 BCs
                if ele.name == "L4 GHB":
                    ele.text="L4 GHB: "+str('{:5.2f}'.format(abs(L4_Q_GHB__inyr)))  # keep separate
                    if (L4_Q_GHB__inyr)<0:
                        ele.text="L4 GHB: "+str('{:5.2f}'.format(abs(L4_Q_GHB__inyr))) 
                        flipRIGHT(ele.name)
                #L5 BCs
                if ele.name == "L5 GHB":
                    ele.text="L5 GHB: "+str('{:5.2f}'.format(abs(L5_Q_GHB__inyr)))  # keep separate
                    if (L5_Q_GHB__inyr)<0:
                        ele.text="L5 GHB: "+str('{:5.2f}'.format(abs(L5_Q_GHB__inyr))) 
                        flipRIGHT(ele.name)

                if ele.text[:9] == "Sim Name:":
                    ele.text="Sim Name: "+str(simnam)+"    "+str(yearval2)

                if ele.text[:8] == "ZB_NAME:":
                    ele.text="ZB_NAME: "+str(ZB_NAME)+"  Number of Cells: " + str(row3[1]) + "  Area Per Cell: 6,250,500 SF"
                if ele.text[:15] == "MassBal Polygon":
                    ele.text="MassBal Polygon: "+str(ZB_NAME)

            #zoom to extent
            sel_exp='ZB_NAME ='+"'"+str(ZB_NAME)+"'"
            df = arcpy.mapping.ListDataFrames(template_mxd)[0]
            for lyr in lyrList:
                if lyr.name == "nfseg_zonebudget_polygons":
                    arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",simnam+'_'+str(yearval2)+'_cbb_poly')
                    lyr.definitionQuery = sel_exp
                    arcpy.SelectLayerByAttribute_management(lyr,"NEW_SELECTION",sel_exp)
                    cal_exp='"'+dir_ZB+"/"+simnam+"__massbal_"+str(ZB_NAME)+"_"+str(yearval2)+".jpg"+'"'
                    arcpy.CalculateField_management(lyr,"ZB_file",cal_exp,"VB","")
                    df.zoomToSelectedFeatures()
                    arcpy.SelectLayerByAttribute_management(lyr,"CLEAR_SELECTION")
                    arcpy.RefreshActiveView()
                    arcpy.mapping.ExportToJPEG(template_mxd,dir_ZB+"/"+simnam+"__massbal_"+str(ZB_NAME)+"_"+str(yearval2)+"_full.jpg",resolution=300)
                    #2017.06.09 trd this was used for the modelwide figure so a quick edited version could be made manually 
                    #template_mxd.saveACopy(cpath_py+"/"+simnam+"__massbal_"+str(ZB_NAME)+"_"+str(yearval2)+".mxd","10.0")
                    lyr.definitionQuery = None
                    #print("quickstop")
                    #exit()

print("completed the entire process")
stop = time.clock()
if (stop-start)>3600:
    print("process completed in:" + str((stop-start)/3600)+' hours.')
elif (stop-start)>60:
    print("process completed in:" + str((stop-start)/60)+' minutes.')
else:
    print("process completed in:" + str((stop-start))+' seconds.')










