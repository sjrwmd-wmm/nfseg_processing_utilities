import arcpy
import sys
import os
import time
arcpy.env.overwriteOutput = True
start = time.clock()
import numpy as np
import fnmatch

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


start = time.clock()


# Get the working PATHs
cpath_py, cpath_py_upper, cpath_py_base = myut.get_current_PATHs()

print("current directory: " + str(cpath_py))
print("parent directory: " + str(cpath_py_upper))
print("grandparent directory: " + str(cpath_py_base))


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
    #arcpy.CreateFileGDB_management(cpath_py,simnam+"_ZB", ARCFILEVERSION)
    print("geodatabase for this sim does not exist - stopping - run s9 cbb_fc first at least")

###check for a sub directory called /ZB, create it if necessary
dir_ZB=str(cpath_py)+"/ZB"
if os.path.exists(dir_ZB) == False:
    os.makedirs(dir_ZB)
else:
    print("subdirectory / ZB directory already exists - existing files will be overwritten without any further warning")
print("root directory for ZB output: "+str(dir_ZB))


###basemap input (static)
base_gdb= (TEMPLATEDIR + "PEST_Baselayers.gdb")
MassBal_poly = (base_gdb + "/nfseg_zonebudget_polygons")

#template_mxd = arcpy.mapping.MapDocument(cpath_py+"/templates/nfseg_zonebudget.mxd")
#lyrList = arcpy.mapping.ListLayers(template_mxd)
#eleList = arcpy.mapping.ListLayoutElements(template_mxd, "TEXT_ELEMENT")

arcpy.SetLogHistory(False)
YEARS=['2001','2009']
for yearval in YEARS:
    print (yearval)
    cbb_fc=gdb+'/nfseg_all_to_cbc_cbc_'+str(yearval)+'_csv'
    if arcpy.Exists(cbb_fc) is False:
        print ("no cbb fc files found in:"+gdb)
        print ("Step C1 must be run - exiting")
        exit()
    else:
        print("found cell-by-cell flow fc for year: "+str(yearval))

        arcpy.MakeFeatureLayer_management(cbb_fc,"cbb_fc_view")
        fields=arcpy.ListFields("cbb_fc_view")
        cbb_poly_fc=gdb+'/'+simnam+'_'+str(yearval)+'_cbb_poly'
        if arcpy.Exists(cbb_poly_fc):
            print("found existing cbb polygon output- removing it then continuing")
            arcpy.Delete_management(cbb_poly_fc)#temp action for debugging
        arcpy.CopyFeatures_management(MassBal_poly,cbb_poly_fc)
        arcpy.MakeFeatureLayer_management(cbb_poly_fc,"cbb_poly_view")
        arcpy.AddField_management("cbb_poly_view","NUMCELLS","LONG","","","","","NULLABLE","NON_REQUIRED","")

        cbb_fieldnames=["ZB_NAME","CONSTANT_HEAD","FLOW_RIGHT_FACE","FLOW_FRONT_FACE","FLOW_LOWER_FACE","WELLS",
                        "DRAINS","RIVER_LEAKAGE","ET","HEAD_DEP_BOUNDS","RECHARGE","MNW2","FLOW_LEFT_FACE",
                        "FLOW_BACK_FACE","FLOW_UPPER_FACE","BALANCE","IBOUND"]
        LAYERS=['01','02','03','04','05','06','07']
        LAYNUMS=[1,2,3,4,5,6,7]

        print ("adding field names")
        for fieldname in cbb_fieldnames:
            #print fieldname
            for laytxt in LAYERS:
                if fieldname!="ZB_NAME":
                    fldname="L"+str(laytxt)+"_"+str(fieldname)
                    arcpy.AddField_management("cbb_poly_view",fldname,"DOUBLE","","","","","NULLABLE","NON_REQUIRED","")

        ###For each CBB poly, select the cbb_pts within it, add the count to NUMCELLS, then compute totals and write to fc
        cbb_poly_fldnames=[]
        skipflds=['OBJECTID','SHAPE','SHAPE_Length','SHAPE_Area','NUMCELLS']
        for fld in arcpy.ListFields("cbb_poly_view"):
            if fld.name not in skipflds:
                cbb_poly_fldnames.append(fld.name)

        ###Get a count of all the cells in each zb polygon
        with arcpy.da.UpdateCursor("cbb_poly_view",cbb_poly_fldnames) as UPDcursor:
            for row in UPDcursor:
                #print row
                ###select all of the cbb_fc values 
                print("Collecting number of cells for ZB_NAME: "+str(row[0]))
                ZBsel_exp="ZB_NAME='"+str(row[0])+"'"
                arcpy.SelectLayerByAttribute_management("cbb_poly_view","NEW_SELECTION",ZBsel_exp)
                arcpy.SelectLayerByLocation_management("cbb_fc_view","WITHIN","cbb_poly_view",0,"NEW_SELECTION")
                cell_ct = int(arcpy.GetCount_management("cbb_fc_view").getOutput(0))/7 # divide by seven for seven layers
                print("cell count: "+str(cell_ct))
                arcpy.CalculateField_management("cbb_poly_view","NUMCELLS",cell_ct,"PYTHON","")
                ##run summary statistics on the selected cbb_fc records, by layer
                tmp_tbl=gdb+'/zb_sumstats_tmp'
                casefield="LAY"
                stats=[]
                for fieldname in cbb_fieldnames:
                    if fieldname!="ZB_NAME":
                        stats.append([fieldname, "Sum"])
                arcpy.Statistics_analysis("cbb_fc_view", tmp_tbl, stats, casefield)
                with arcpy.da.SearchCursor(tmp_tbl,[fld.name for fld in arcpy.ListFields(tmp_tbl)]) as SRCcursor:
                    for SRCrow in SRCcursor:
                        itm_ct=2
                        for fieldname in cbb_fieldnames:
                            if fieldname!="ZB_NAME":
                                itm_ct=itm_ct+1
                                laytxt='{0:02d}'.format(SRCrow[1])
                                arcpy.CalculateField_management("cbb_poly_view",('L'+str(laytxt)+'_'+fieldname),SRCrow[itm_ct],"PYTHON","")
                arcpy.Delete_management(tmp_tbl)
        arcpy.SelectLayerByAttribute_management("cbb_poly_view","CLEAR_SELECTION")
        arcpy.SelectLayerByAttribute_management("cbb_fc_view","CLEAR_SELECTION")
        ###completed the creation and population of zone budget by polygon file "cbb_poly_view"

        ##Add and Compute Lateral Flow Summation fields, also append to cbb_fieldnames
        filtered = fnmatch.filter(cbb_poly_fldnames, '*FLOW_RIGHT_FACE*')
        for filterval in filtered:
            layer_prefix=filterval[:4]
            #print layer_prefix
            New_fldname=filterval.replace('FLOW_RIGHT_FACE','FLOW_LATERAL_NET')
            arcpy.AddField_management("cbb_poly_view",New_fldname,"DOUBLE","","","","","NULLABLE","NON_REQUIRED","")

            rght=str(layer_prefix)+'FLOW_RIGHT_FACE'
            frnt=str(layer_prefix)+'FLOW_FRONT_FACE'
            left=str(layer_prefix)+'FLOW_LEFT_FACE'
            back=str(layer_prefix)+'FLOW_BACK_FACE'
            cal_exp="-["+rght+"] - ["+frnt+"] + ["+left+"] + ["+back+"]"
            arcpy.CalculateField_management("cbb_poly_view",New_fldname,cal_exp,"VB","")


stop = time.clock()
if (stop-start)>3600:
    print("part1 completed in:" + str((stop-start)/3600)+' hours.')
elif (stop-start)>60:
    print("part1 completed in:" + str((stop-start)/60)+' minutes.')
else:
    print("part1 completed in:" + str((stop-start))+' seconds.')
arcpy.SetLogHistory(True)
###Completed Creating  the ZB polygon data

print("completed the entire process")
stop = time.clock()
if (stop-start)>3600:
    print("process completed in:" + str((stop-start)/3600)+' hours.')
elif (stop-start)>60:
    print("process completed in:" + str((stop-start)/60)+' minutes.')
else:
    print("process completed in:" + str((stop-start))+' seconds.')

