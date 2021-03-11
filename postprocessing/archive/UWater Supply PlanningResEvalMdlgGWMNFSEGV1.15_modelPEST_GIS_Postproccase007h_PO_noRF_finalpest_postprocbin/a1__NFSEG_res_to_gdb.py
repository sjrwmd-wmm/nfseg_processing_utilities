import arcpy
import sys
import os
import time
arcpy.env.overwriteOutput = True
start = time.clock()

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

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

template_hds = arcpy.mapping.MapDocument(cpath_py + "/templates/nfseg_PEST_template.mxd")

###basemap input (static)
base_gdb=cpath_py+"/templates/PEST_Baselayers.gdb"
WL_targets = "WL_template"
VHD_L1L3_targets = "VHD_L1to3_template"
gage_targets = "gage_template"
gageQR_targets = "NFSEG_lu_gageInt"
gageQS_targets = "qs_targets_template"
gage_poly_NCB = "GAGE_Polys_NoClosedBasins_template"
# start revisions for VHD 3-5
VHD_L3L5_targets = "VHD_L3to5_template"
springs_targets = "NFSEG_Springs"
springs_1st = "NFSEG_Springs_1stMag"
HHD_L3_targets_01 = "HHD_L3_01_template"
HHD_L3_targets_09 = "HHD_L3_09_template"

#find PEST output file (*.res) in the upper directory - the rest of the files get named with the res file name in it
num_simnams=0
for file in os.listdir(cpath_py_upper):
    if str(file[-3:])=='res':
        simnam=file[:-4]
        num_simnams=num_simnams+1
if num_simnams==0:
    print("no *.res file found - stopping")
    exit()
elif num_simnams>1:
    print("multiple *.res files found in this folder - stopping")
    exit()
else:
    print("sim name:"+str(simnam))
#read the rei file as lines
res_file=cpath_py_upper+"/"+str(simnam)+".res"
with open(res_file, mode='r') as res:
    res_lines=res.readlines()

#setup geodatabase based on simnam
gdb=cpath_py+"/"+simnam+".gdb"
if arcpy.Exists(gdb):
    print("geodatabase of this sim already exists - files inside will be overwritten")
else:
    arcpy.CreateFileGDB_management(cpath_py,simnam,"9.3")
    print("Output geodatabase set up")

## create the res table schema
if arcpy.Exists(gdb+"/res"):
    arcpy.Delete_management(gdb+"/res")
arcpy.CreateTable_management(gdb,"res","#","#")
arcpy.MakeTableView_management(gdb+"/"+"res","res_view")
arcpy.AddField_management("res_view","Name","TEXT","#","#","50","Name","NULLABLE","NON_REQUIRED","#")
arcpy.AddField_management("res_view","Group_","TEXT","#","#","50","Group_","NULLABLE","NON_REQUIRED","#")
arcpy.AddField_management("res_view","Measured","DOUBLE","#","#","#","Measured","NULLABLE","NON_REQUIRED","#")
arcpy.AddField_management("res_view","Modelled","DOUBLE","#","#","#","Modelled","NULLABLE","NON_REQUIRED","#")
arcpy.AddField_management("res_view","Residual","DOUBLE","#","#","#","Residual","NULLABLE","NON_REQUIRED","#")
arcpy.AddField_management("res_view","Weight","DOUBLE","#","#","#","Weight","NULLABLE","NON_REQUIRED","#")
arcpy.AddField_management("res_view","Wgt_text","TEXT","#","#","50","Wgt_text","NULLABLE","NON_REQUIRED","#")
arcpy.AddField_management("res_view","PEST_Run","TEXT","#","#","50","PEST_Run","NULLABLE","NON_REQUIRED","#")

###copy the targets to the new gdb
arcpy.MakeFeatureLayer_management(base_gdb+"/"+WL_targets,"WL_targets_view")
arcpy.MakeFeatureLayer_management(base_gdb+"/"+VHD_L1L3_targets,"VHD_L1L3_targets_view")
arcpy.MakeFeatureLayer_management(base_gdb+"/"+VHD_L3L5_targets,"VHD_L3L5_targets_view")
arcpy.MakeFeatureLayer_management(base_gdb+"/"+gage_targets,"gage_targets_view")
arcpy.MakeFeatureLayer_management(base_gdb+"/"+springs_targets,"springs_targets_view")
arcpy.MakeFeatureLayer_management(base_gdb+"/"+springs_1st,"springs_1st_view")
arcpy.MakeFeatureLayer_management(base_gdb+"/"+gageQR_targets,"gageQR_targets_view")
arcpy.MakeFeatureLayer_management(base_gdb+"/"+gageQS_targets,"gageQS_targets_view")
arcpy.MakeFeatureLayer_management(base_gdb+"/"+gage_poly_NCB,"gage_poly_NCB_view")
arcpy.MakeFeatureLayer_management(base_gdb+"/"+HHD_L3_targets_01,"HHD_L3_targets_01_view")
arcpy.MakeFeatureLayer_management(base_gdb+"/"+HHD_L3_targets_09,"HHD_L3_targets_09_view")

## new code for res table.
#populate res_gdb table from the res_lines
res_fields = ['Name', 'Group_', 'Measured', 'Modelled', 'Residual', 'Weight', 'Wgt_text']
#'Weight_Measured','Weight_Modelled', 'Weight_Residual', 'Measurement_sd', 'Natural_weight', ]
with arcpy.da.InsertCursor("res_view",res_fields) as cursor:
    lc=0
    read_flg=0
    for line in res_lines:
        lc=lc+1
        values=line.split()
        values2 = [values[0],values[1],values[2],values[3],values[4],values[5]]
        if len(values)==0:
            print("blankline at line:"+str(lc))
        elif values2[0]=="Name":
            print("begin reading data on line:"+str(lc+1))
            read_flg=1
        elif read_flg==1:
            if is_number(values2[5]): # standard output, 6th - 12th items is a numerical weight calcs.
                values2.append("na") # append "na" to the column in this case
                cursor.insertRow(values2)
            else:
                mnl_vals=[]
                for i in range(0,5):
                    mnl_vals.append(values2[i])
                mnl_vals.append("0") #make the numerical weight column zero
                mnl_vals.append("covmat")
                cursor.insertRow(mnl_vals)

arcpy.CalculateField_management("res_view","PEST_Run",'"'+simnam+'"',"PYTHON","#")

arcpy.env.qualifiedFieldNames = False #  uncheck the box
#2001 res WL_targets
arcpy.AddJoin_management("WL_targets_view","WLID01","res_view","Name","KEEP_ALL")
arcpy.SelectLayerByAttribute_management("WL_targets_view","NEW_SELECTION","res.Name is not null")
arcpy.FeatureClassToFeatureClass_conversion("WL_targets_view",gdb,simnam+"_WL_targets_2001")
arcpy.RemoveJoin_management("WL_targets_view","#")
arcpy.SelectLayerByAttribute_management("WL_targets_view","CLEAR_SELECTION")

#2009 res WL_targets
arcpy.AddJoin_management("WL_targets_view","WLID09","res_view","Name","KEEP_ALL")
arcpy.SelectLayerByAttribute_management("WL_targets_view","NEW_SELECTION","res.Name is not null")
arcpy.FeatureClassToFeatureClass_conversion("WL_targets_view",gdb,simnam+"_WL_targets_2009")
arcpy.RemoveJoin_management("WL_targets_view","#")
arcpy.SelectLayerByAttribute_management("WL_targets_view","CLEAR_SELECTION")

#2001 res VHD_L1L3_targets
arcpy.AddJoin_management("VHD_L1L3_targets_view","VDID01","res_view","Name","KEEP_ALL")
arcpy.SelectLayerByAttribute_management("VHD_L1L3_targets_view","NEW_SELECTION","res.Name is not null")
arcpy.FeatureClassToFeatureClass_conversion("VHD_L1L3_targets_view",gdb,simnam+"_VHD_L1L3_targets_2001")
arcpy.RemoveJoin_management("VHD_L1L3_targets_view","#")
arcpy.SelectLayerByAttribute_management("VHD_L1L3_targets_view","CLEAR_SELECTION")

#2009 res VHD_L1L3_targets
arcpy.AddJoin_management("VHD_L1L3_targets_view","VDID09","res_view","Name","KEEP_ALL")
arcpy.SelectLayerByAttribute_management("VHD_L1L3_targets_view","NEW_SELECTION","res.Name is not null")
arcpy.FeatureClassToFeatureClass_conversion("VHD_L1L3_targets_view",gdb,simnam+"_VHD_L1L3_targets_2009")
arcpy.RemoveJoin_management("VHD_L1L3_targets_view","#")
arcpy.SelectLayerByAttribute_management("VHD_L1L3_targets_view","CLEAR_SELECTION")

#2001 res VHD_L3L5_targets
arcpy.AddJoin_management("VHD_L3L5_targets_view","VDID01","res_view","Name","KEEP_ALL")
arcpy.SelectLayerByAttribute_management("VHD_L3L5_targets_view","NEW_SELECTION","res.Name is not null")
arcpy.FeatureClassToFeatureClass_conversion("VHD_L3L5_targets_view",gdb,simnam+"_VHD_L3L5_targets_2001")
arcpy.RemoveJoin_management("VHD_L3L5_targets_view","#")
arcpy.SelectLayerByAttribute_management("VHD_L3L5_targets_view","CLEAR_SELECTION")
#2009 res VHD_L3L5_targets
arcpy.AddJoin_management("VHD_L3L5_targets_view","VDID09","res_view","Name","KEEP_ALL")
arcpy.SelectLayerByAttribute_management("VHD_L3L5_targets_view","NEW_SELECTION","res.Name is not null")
arcpy.FeatureClassToFeatureClass_conversion("VHD_L3L5_targets_view",gdb,simnam+"_VHD_L3L5_targets_2009")
arcpy.RemoveJoin_management("VHD_L3L5_targets_view","#")
arcpy.SelectLayerByAttribute_management("VHD_L3L5_targets_view","CLEAR_SELECTION")

# HHD targets
# 2001
arcpy.AddJoin_management("HHD_L3_targets_01_view","head_diff_","res_view","Name","KEEP_ALL")
arcpy.SelectLayerByAttribute_management("HHD_L3_targets_01_view","NEW_SELECTION","res.Name is not null")
arcpy.FeatureClassToFeatureClass_conversion("HHD_L3_targets_01_view",gdb,simnam+"_HHD_L3_targets_01")
arcpy.RemoveJoin_management("HHD_L3_targets_01_view","#")
arcpy.SelectLayerByAttribute_management("HHD_L3_targets_01_view","CLEAR_SELECTION")
# 2009
arcpy.AddJoin_management("HHD_L3_targets_09_view","head_diff_","res_view","Name","KEEP_ALL")
arcpy.SelectLayerByAttribute_management("HHD_L3_targets_09_view","NEW_SELECTION","res.Name is not null")
arcpy.FeatureClassToFeatureClass_conversion("HHD_L3_targets_09_view",gdb,simnam+"_HHD_L3_targets_09")
arcpy.RemoveJoin_management("HHD_L3_targets_09_view","#")
arcpy.SelectLayerByAttribute_management("HHD_L3_targets_09_view","CLEAR_SELECTION")

arcpy.env.qualifiedFieldNames = True #  uncheck the box the rest of the layers below have the join name in them. 
#note to self to fix this part and update the MXD def queries

#join the res_gdb to the gage_targets_view layer and export as new fcs (do once for each year 2001, 2009 ; qs and qr)
#20012009 qr res gage_targets_view - for OBR figures
arcpy.AddJoin_management("gageQR_targets_view","obs_name","res_view","Name","KEEP_ALL")
arcpy.SelectLayerByAttribute_management("gageQR_targets_view","NEW_SELECTION","res.Name is not null")
if arcpy.Exists(gdb+"/"+simnam+"_qr_20012009"):
    arcpy.Delete_management(gdb+"/"+simnam+"_qr_20012009")
arcpy.FeatureClassToFeatureClass_conversion("gageQR_targets_view",gdb,simnam+"_qr_20012009")
arcpy.AddField_management(gdb+"/"+simnam+"_qr_20012009","RES_PCT","DOUBLE","#","#","#","#","NULLABLE","NON_REQUIRED","#")
arcpy.CalculateField_management(gdb+"/"+simnam+"_qr_20012009","RES_PCT","[res_Residual] / [res_Measured] * 100","VB","#")
arcpy.RemoveJoin_management("gageQR_targets_view","#")
arcpy.SelectLayerByAttribute_management("gageQR_targets_view","CLEAR_SELECTION")

#2001 qr res gage_targets_view
arcpy.AddJoin_management("gage_targets_view","qr01","res_view","Name","KEEP_ALL")
arcpy.SelectLayerByAttribute_management("gage_targets_view","NEW_SELECTION","res.Name is not null")
arcpy.FeatureClassToFeatureClass_conversion("gage_targets_view",gdb,simnam+"_qr_2001")
arcpy.AddField_management(gdb+"/"+simnam+"_qr_2001","RES_PCT","DOUBLE","#","#","#","#","NULLABLE","NON_REQUIRED","#")
arcpy.CalculateField_management(gdb+"/"+simnam+"_qr_2001","RES_PCT","[res_Residual] / [res_Measured] * 100","VB","#")
arcpy.RemoveJoin_management("gage_targets_view","#")
arcpy.SelectLayerByAttribute_management("gage_targets_view","CLEAR_SELECTION")

#2009 qr res gage_targets_view
arcpy.AddJoin_management("gage_targets_view","qr09","res_view","Name","KEEP_ALL")
arcpy.SelectLayerByAttribute_management("gage_targets_view","NEW_SELECTION","res.Name is not null")
arcpy.FeatureClassToFeatureClass_conversion("gage_targets_view",gdb,simnam+"_qr_2009")
arcpy.AddField_management(gdb+"/"+simnam+"_qr_2009","RES_PCT","DOUBLE","#","#","#","#","NULLABLE","NON_REQUIRED","#")
arcpy.CalculateField_management(gdb+"/"+simnam+"_qr_2009","RES_PCT","[res_Residual] / [res_Measured] * 100","VB","#")
arcpy.RemoveJoin_management("gage_targets_view","#")
arcpy.SelectLayerByAttribute_management("gage_targets_view","CLEAR_SELECTION")

#qs targets
#20012009 qs res gage_targets_view - for OBR figures
arcpy.AddJoin_management("gageQS_targets_view","obs_name","res_view","Name","KEEP_ALL")
arcpy.SelectLayerByAttribute_management("gageQS_targets_view","NEW_SELECTION","res.Name is not null")
if arcpy.Exists(gdb+"/"+simnam+"_qs_20012009"):
    arcpy.Delete_management(gdb+"/"+simnam+"_qs_20012009")
arcpy.FeatureClassToFeatureClass_conversion("gageQS_targets_view",gdb,simnam+"_qs_20012009")
arcpy.AddField_management(gdb+"/"+simnam+"_qs_20012009","RES_PCT","DOUBLE","#","#","#","#","NULLABLE","NON_REQUIRED","#")
arcpy.CalculateField_management(gdb+"/"+simnam+"_qs_20012009","RES_PCT","[res_Residual] / [res_Measured] * 100","VB","#")
arcpy.RemoveJoin_management("gageQS_targets_view","#")
arcpy.SelectLayerByAttribute_management("gageQS_targets_view","CLEAR_SELECTION")

#2001 qs res gage_targets_view
arcpy.AddJoin_management("gage_targets_view","qs01","res_view","Name","KEEP_ALL")
arcpy.SelectLayerByAttribute_management("gage_targets_view","NEW_SELECTION","res.Name is not null")
arcpy.FeatureClassToFeatureClass_conversion("gage_targets_view",gdb,simnam+"_qs_2001")
arcpy.AddField_management(gdb+"/"+simnam+"_qs_2001","RES_PCT","DOUBLE","#","#","#","#","NULLABLE","NON_REQUIRED","#")
arcpy.CalculateField_management(gdb+"/"+simnam+"_qs_2001","RES_PCT","[res_Residual] / [res_Measured] * 100","VB","#")
arcpy.RemoveJoin_management("gage_targets_view","#")
arcpy.SelectLayerByAttribute_management("gage_targets_view","CLEAR_SELECTION")

#2009 qs res gage_targets_view
arcpy.AddJoin_management("gage_targets_view","qs09","res_view","Name","KEEP_ALL")
arcpy.SelectLayerByAttribute_management("gage_targets_view","NEW_SELECTION","res.Name is not null")
arcpy.FeatureClassToFeatureClass_conversion("gage_targets_view",gdb,simnam+"_qs_2009")
arcpy.AddField_management(gdb+"/"+simnam+"_qs_2009","RES_PCT","DOUBLE","#","#","#","#","NULLABLE","NON_REQUIRED","#")
arcpy.CalculateField_management(gdb+"/"+simnam+"_qs_2009","RES_PCT","[res_Residual] / [res_Measured] * 100","VB","#")
arcpy.RemoveJoin_management("gage_targets_view","#")
arcpy.SelectLayerByAttribute_management("gage_targets_view","CLEAR_SELECTION")

#gaged polygons - NCB (no closed basins) includes both qs/qr and 01/09 PEST target info
arcpy.AddJoin_management("gage_poly_NCB_view","obs_name","res_view","Name","KEEP_ALL")
arcpy.SelectLayerByAttribute_management("gage_poly_NCB_view","NEW_SELECTION","res.Name is not null")
if arcpy.Exists(gdb+"/"+simnam+"_qrqs_gagepoly_NCB"):
    arcpy.Delete_management(gdb+"/"+simnam+"_qrqs_gagepoly_NCB")
arcpy.FeatureClassToFeatureClass_conversion("gage_poly_NCB_view",gdb,simnam+"_qrqs_gagepoly_NCB")
arcpy.AddField_management(gdb+"/"+simnam+"_qrqs_gagepoly_NCB","RES_PCT","DOUBLE","#","#","#","#","NULLABLE","NON_REQUIRED","#")
arcpy.CalculateField_management(gdb+"/"+simnam+"_qrqs_gagepoly_NCB","RES_PCT","[res_Residual] / [res_Measured] * 100","VB","#")
arcpy.RemoveJoin_management("gage_poly_NCB_view","#")
arcpy.SelectLayerByAttribute_management("gage_poly_NCB_view","CLEAR_SELECTION")

#2017.01.18 SPRINGS
#2001 qsprings res gage_targets_view
arcpy.AddJoin_management("springs_targets_view","Springs_SiteID01","res_view","Name","KEEP_ALL")
arcpy.SelectLayerByAttribute_management("springs_targets_view","NEW_SELECTION","res.Name is not null")
arcpy.FeatureClassToFeatureClass_conversion("springs_targets_view",gdb,simnam+"_qsprings_2001")
arcpy.AddField_management(gdb+"/"+simnam+"_qsprings_2001","RES_PCT","DOUBLE","#","#","#","#","NULLABLE","NON_REQUIRED","#")
with arcpy.da.UpdateCursor(gdb+"/"+simnam+"_qsprings_2001",["res_Measured","res_Residual","RES_PCT"]) as cursor:
    for row in cursor:
        if row[0]<>0:
            row[2]=row[1]/row[0]
            cursor.updateRow(row)
#arcpy.CalculateField_management(gdb+"/"+simnam+"_qsprings_2001","RES_PCT","[Residual] / [Measured] * 100","VB","#")
arcpy.RemoveJoin_management("springs_targets_view","#")
arcpy.SelectLayerByAttribute_management("springs_targets_view","CLEAR_SELECTION")

#2009 qsprings res gage_targets_view
arcpy.AddJoin_management("springs_targets_view","Springs_SiteID09","res_view","Name","KEEP_ALL")
arcpy.SelectLayerByAttribute_management("springs_targets_view","NEW_SELECTION","res.Name is not null")
arcpy.FeatureClassToFeatureClass_conversion("springs_targets_view",gdb,simnam+"_qsprings_2009")
arcpy.AddField_management(gdb+"/"+simnam+"_qsprings_2009","RES_PCT","DOUBLE","#","#","#","#","NULLABLE","NON_REQUIRED","#")
with arcpy.da.UpdateCursor(gdb+"/"+simnam+"_qsprings_2009",["res_Measured","res_Residual","RES_PCT"]) as cursor:
    for row in cursor:
        if row[0]<>0:
            row[2]=row[1]/row[0]
            cursor.updateRow(row)
arcpy.RemoveJoin_management("springs_targets_view","#")
arcpy.SelectLayerByAttribute_management("springs_targets_view","CLEAR_SELECTION")
arcpy.env.qualifiedFieldNames = True #  uncheck the box

#2001 1st order springs
arcpy.AddJoin_management("springs_1st_view","PestID01","res_view","Name","KEEP_ALL")
arcpy.SelectLayerByAttribute_management("springs_1st_view","NEW_SELECTION","res.Name is not null")
arcpy.FeatureClassToFeatureClass_conversion("springs_1st_view",gdb,simnam+"_qsprings_1st_2001")
arcpy.AddField_management(gdb+"/"+simnam+"_qsprings_1st_2001","RES_PCT","DOUBLE","#","#","#","#","NULLABLE","NON_REQUIRED","#")
with arcpy.da.UpdateCursor(gdb+"/"+simnam+"_qsprings_1st_2001",["res_Measured","res_Residual","RES_PCT"]) as cursor:
    for row in cursor:
        if row[0]<>0:
            row[2]=row[1]/row[0]
            cursor.updateRow(row)
arcpy.RemoveJoin_management("springs_1st_view","#")
arcpy.SelectLayerByAttribute_management("springs_1st_view","CLEAR_SELECTION")

#2009 1st order springs
arcpy.AddJoin_management("springs_1st_view","PestID09","res_view","Name","KEEP_ALL")
arcpy.SelectLayerByAttribute_management("springs_1st_view","NEW_SELECTION","res.Name is not null")
arcpy.FeatureClassToFeatureClass_conversion("springs_1st_view",gdb,simnam+"_qsprings_1st_2009")
arcpy.AddField_management(gdb+"/"+simnam+"_qsprings_1st_2009","RES_PCT","DOUBLE","#","#","#","#","NULLABLE","NON_REQUIRED","#")
with arcpy.da.UpdateCursor(gdb+"/"+simnam+"_qsprings_1st_2009",["res_Measured","res_Residual","RES_PCT"]) as cursor:
    for row in cursor:
        if row[0]<>0:
            row[2]=row[1]/row[0]
            cursor.updateRow(row)
arcpy.RemoveJoin_management("springs_1st_view","#")
arcpy.SelectLayerByAttribute_management("springs_1st_view","CLEAR_SELECTION")

stop = time.clock()
DUR=round((stop-start)/60,1)
print("Script a1 completed in "+str(DUR)+" min")


