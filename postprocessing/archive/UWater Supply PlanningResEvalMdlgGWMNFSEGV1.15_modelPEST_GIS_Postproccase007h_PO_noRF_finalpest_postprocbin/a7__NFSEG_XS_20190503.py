import arcpy
import sys
import os
import time
arcpy.env.overwriteOutput = True
start = time.clock()
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.cbook import get_sample_data

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

###props
props=gdb+'/'+'nfseg_props'


###check for a sub directory called /XS, create it if necessary
dir_XS=str(cpath_py)+"/XS"
if os.path.exists(dir_XS) == False:
    os.makedirs(dir_XS)
else:
    print("subdirectory / XS directory already exists - existing files will get overwritten without any further warning")
print("root directory for XS output: "+str(dir_XS))


###basemap input (static)
base_gdb=cpath_py+"/templates/PEST_Baselayers.gdb"
nfseg_active_grid_poly=base_gdb+"/NFSEGActiveGrid_Albers_ROWCOL_LM"
### the followings was prepared just for this script.  it is the centroids of each of the active grid
### values from rasters for UFA pot surface 2001 and 2009, and 10k TDS boundary extracted as add'l fields
nfseg_active_grid_cent=base_gdb+"/NFSEGActiveGrid_Albers_ROWCOL_cent"
### some work to set up the IBND table in this gdb
NLAY=7
NROW=752
NCOL=704
#IBND_inf=[]
#for row in range(1,int(NROW)+1):
#    curcol=0
#    while curcol<(int(NCOL)):
#        curcol=curcol+1
#        IBND_inf.append(str(row)+"_"+str(curcol))
#for i in range(1,NLAY+1):
#    iter_ct=0
#    with open("D:/00Temp/040617nfseg17ph1r3/nfseg_pest_postproc/templates/ibound"+str(i)+".inf","r") as inf:
#        for row in range(1,int(NROW)+1):
#            curcol=0
#            #print row
#            while curcol<(int(NCOL)):
#                dataline=inf.readline()
#                linevalues=dataline.split()
#                for value in linevalues:
#                    curcol=curcol+1
#                    IBND_inf[iter_ct]=str(IBND_inf[iter_ct])+","+str(value)
#                    iter_ct=iter_ct+1
#
#with arcpy.da.InsertCursor("ibnd_tbl_view",['ROW_COL','ibnd1','ibnd2','ibnd3','ibnd4','ibnd5','ibnd6','ibnd7']) as cursor99:
#    for propline in IBND_inf:
#        propdata=propline.split(',')
#        cursor99.insertRow(propdata)

ibnd=base_gdb+'/nfseg_ibnd'

###here are the XS lines, uses field 'XS_name' to identify in files.
XSlines="nfseg_xslines"

###MAIN
arcpy.MakeFeatureLayer_management(nfseg_active_grid_poly,"grid_poly_view")
arcpy.MakeFeatureLayer_management(base_gdb+'/XSlines/'+XSlines,"XSlines_view")

###separate the XS lines at vertexes (note topology defined in feature dataset which automatically adds a vertex wherever a line
###....interects with the model grid.
arcpy.SplitLine_management("XSlines_view",gdb+'/'+XSlines+'_data')
arcpy.MakeFeatureLayer_management(gdb+'/'+XSlines+'_data',"XSdata_view")

arcpy.AddField_management("XSdata_view","XS_dist","DOUBLE","","","","","NULLABLE","NON_REQUIRED","")
arcpy.AddField_management("XSdata_view","ROW_COL","TEXT","","","10","","NULLABLE","NON_REQUIRED","")
#arcpy.Intersect_analysis("XSlines_view #;grid_poly_view #", gdb+'/'+XSlines+'_data',"ALL","-1 Unknown","INPUT")
with arcpy.da.UpdateCursor("XSdata_view",['XS_name','SHAPE_Length','XS_dist']) as cursor1:
    XS_name_prev="zzz"
    TOT_DIST=0
    for row in cursor1:
        if row[0]<>XS_name_prev:
            TOT_DIST=row[1]
        else:
            TOT_DIST=TOT_DIST+row[1]
        row[2]=TOT_DIST
        cursor1.updateRow(row)
        XS_name_prev = row[0]

arcpy.SpatialJoin_analysis("XSdata_view","grid_poly_view", gdb+"/xs_sj_temp", "JOIN_ONE_TO_ONE", "KEEP_ALL", "", "WITHIN", "", "")
arcpy.AddJoin_management("XSdata_view","OBJECTID",gdb+"/xs_sj_temp","OBJECTID","KEEP_ALL")
arcpy.SelectLayerByAttribute_management("XSdata_view","NEW_SELECTION","xs_sj_temp.ROW_COL_1 is not null")
arcpy.CalculateField_management("XSdata_view", "nfseg_xslines_data.ROW_COL", "!xs_sj_temp.ROW_COL_1!", "PYTHON_9.3", "")
arcpy.RemoveJoin_management("XSdata_view","#")
arcpy.SelectLayerByAttribute_management("XSdata_view","SWITCH_SELECTION")
arcpy.DeleteFeatures_management("XSdata_view")
arcpy.Delete_management(gdb+"/xs_sj_temp")

XS={}
with arcpy.da.UpdateCursor("XSdata_view",'XS_name') as cursor:
    for row in cursor:
        XS[row[0]]=1

### get IBND data as a lookup
arcpy.MakeTableView_management(ibnd,"ibnd_tbl_view")
ibnd_fields=['ROW_COL','ibnd1','ibnd2','ibnd3','ibnd4','ibnd5','ibnd6','ibnd7']
ibnd_lu={}
with arcpy.da.SearchCursor("ibnd_tbl_view",ibnd_fields)as cursor6:
    for row in cursor6:
        ibnd_lu[row[0]]=row


### get model props data as a lookup
arcpy.MakeFeatureLayer_management(props,"props_view")
props_fields=['ref_ROW_COL','ref_L1Top','ref_L1Bot','ref_L2Bot','ref_L3Bot',
              'ref_L4Bot','ref_L5Bot','ref_L6Bot','ref_L7Bot']
props_lu={}
with arcpy.da.SearchCursor("props_view",props_fields)as cursor2:
    for row in cursor2:
        props_lu[row[0]]=row
### add fields for model props
for fieldname in props_fields:
    if fieldname<>'ref_ROW_COL':
        arcpy.AddField_management("XSdata_view",fieldname,"DOUBLE","","","","","NULLABLE","NON_REQUIRED","")
### now populate the XS lines with it, if IBND = zero, return the previous bottom value
xsprops_fields=['ROW_COL','ref_L1Top','ref_L1Bot','ref_L2Bot','ref_L3Bot',
              'ref_L4Bot','ref_L5Bot','ref_L6Bot','ref_L7Bot']
with arcpy.da.UpdateCursor("XSdata_view",xsprops_fields)as cursor3:
    for row in cursor3:
        props=props_lu[row[0]]
        ibnds=ibnd_lu[row[0]]
        for i in range(1,9):
            if i==1: #..if we are reading ref_L1Top
                if ibnds[i]==0:
                    row[i]=None
                else:
                    row[i]=props[i]
            else:
                if ibnds[i-1]==0:
                    row[i]=row[i-1]
                else:
                    row[i]=props[i]
        cursor3.updateRow(row)

### get attrributes from grid cent as a lookup
arcpy.MakeFeatureLayer_management(nfseg_active_grid_cent,"grid_cent_view")
cent_fields=['ROW_COL','ps2001_GCerased_raster','ps2009_GCerased_raster','Revised_10000_TDS_Boundary_JAS20140129']
### add fields for cent props
for fieldname in cent_fields:
    if fieldname<>'ROW_COL':
        arcpy.AddField_management("XSdata_view",fieldname,"DOUBLE","","","","","NULLABLE","NON_REQUIRED","")
cent_lu={}
with arcpy.da.SearchCursor("grid_cent_view",cent_fields)as cursor22:
    for row in cursor22:
       cent_lu[row[0]]=row
### now populate the XS lines with it, 
with arcpy.da.UpdateCursor("XSdata_view",cent_fields)as cursor33:
    for row in cursor33:
        row[1]=cent_lu[row[0]][1]
        row[2]=cent_lu[row[0]][2]
        row[3]=cent_lu[row[0]][3]
        cursor33.updateRow(row)
###building data for XS complete.


###dissolve the data lines now (to remove parts of the XS line that may fall outside the active model boundary
arcpy.Dissolve_management("XSdata_view", gdb+'/'+simnam+'_XS_lines',"XS_name","","MULTI_PART","DISSOLVE_LINES")
arcpy.AddField_management(gdb+'/'+simnam+'_XS_lines',"XS_file","TEXT","","","200","","NULLABLE","NON_REQUIRED","")
# Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
# The following inputs are layers or table views: "case_003_optimal_parms_XS_lines"
cal_Exp='"'+dir_XS+'/'+str(simnam)+'_"+'+"str(!XS_name!)"+'+".png"'
arcpy.CalculateField_management(gdb+'/'+simnam+'_XS_lines',"XS_file",cal_Exp,"PYTHON_9.3", code_block="")


XSFLDS_ALL=['XS_dist','ref_L1Top','ref_L1Bot','ref_L2Bot','ref_L3Bot','ref_L4Bot','ref_L5Bot','ref_L6Bot','ref_L7Bot',
            'ps2001_GCerased_raster','ps2009_GCerased_raster',
            'Revised_10000_TDS_Boundary_JAS20140129','XS_ID']


mxd=arcpy.mapping.MapDocument(cpath_py+"/templates/nfseg_XSlocmap.mxd")
df = arcpy.mapping.ListDataFrames(mxd)[0]
LayList = arcpy.mapping.ListLayers(mxd)

for xsi in XS:
    print("processing: "+str(xsi))
    #create a location map for the XS
    for lyr in LayList:
        if lyr.name=="XS lines":
            arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",simnam+'_XS_lines')
            lyr.definitionQuery = "XS_Name = '"+xsi+"'"
            sel_exp=""""XS_name" = '"""+str(xsi)+ """'"""
            arcpy.SelectLayerByAttribute_management(lyr,"NEW_SELECTION",sel_exp)
            df.zoomToSelectedFeatures()
            arcpy.SelectLayerByAttribute_management(lyr,"CLEAR_SELECTION")
        if lyr.name=="nfseg_xslines_data":
            arcpy.mapping.Layer.replaceDataSource(lyr,gdb,"FILEGDB_WORKSPACE",'nfseg_xslines_data')
            lyr.definitionQuery = "XS_Name = '"+xsi+"'"
    for lyr in LayList:
        if lyr.name=="XS lines":
            arcpy.mapping.ExportToPNG(mxd, dir_XS+'/'+simnam+'_'+xsi+"_locmap.png",resolution=200)

    arcpy.SelectLayerByAttribute_management("XSdata_view","NEW_SELECTION",""""XS_name" = '"""+str(xsi)+ """'""")
    Xvals=[]
    l1top=[]
    l1bot=[]
    l2bot=[]
    l3bot=[]
    l4bot=[]
    l5bot=[]
    l6bot=[]
    l7bot=[]
    p2001=[]
    p2009=[]
    tds10k=[]
    with arcpy.da.SearchCursor("XSdata_view",XSFLDS_ALL) as cursor40:
        for row in cursor40:
            Xvals.append(row[0])
            l1top.append(row[1])
            l1bot.append(row[2])
            l2bot.append(row[3])
            l3bot.append(row[4])
            l4bot.append(row[5])
            l5bot.append(row[6])
            l6bot.append(row[7])
            l7bot.append(row[8])
            p2001.append(row[9])
            p2009.append(row[10])
            tds10k.append(row[11])
            XSID=row[12]


    fig=plt.figure()
    ax=plt.subplot(111)

    matplotlib.rcParams.update({'font.size': 8})
    axis_font = {'fontname':'Arial', 'size':'8'}

    plt.fill_between(Xvals,l1top,l1bot,color='khaki', label="L1 - SAS")
    plt.fill_between(Xvals,l1bot,l2bot,color='olive', label="L2 - ICU")
    plt.fill_between(Xvals,l2bot,l3bot,color='skyblue', label="L3 - UFA")
    plt.fill_between(Xvals,l3bot,l4bot,color='saddlebrown', label="L4 - MCU")
    plt.fill_between(Xvals,l4bot,l5bot,color='darkcyan', label="L5 - LFA1")
    plt.fill_between(Xvals,l5bot,l6bot,color='coral', label="L6 - LCU")
    plt.fill_between(Xvals,l6bot,l7bot,color='mediumseagreen', label="L7 - LFA2")
    plt.plot(Xvals, p2001, color='magenta', label="FAS pot surface 2001")
    plt.plot(Xvals, p2009, color='cyan', label="FAS pot surface 2009")
    plt.plot(Xvals, tds10k, color='black', label="TDS 10k")
    plt.ylabel("Elevation (ft navd88)",fontsize=8)
    plt.xlabel("Distance (m)",fontsize=8)
    plt.xlim(xmax=max(Xvals))
    plt.annotate(XSID, xy=(0,1.05), xycoords='axes fraction', fontsize=12)
    plt.annotate((str(XSID)+"'"), xy=(0.98,1.05), xycoords='axes fraction', fontsize=12)
    #A=0,max(Xvals)
    #B=max(l1top)+50,max(l1top)+50
    #C=XSID, str(XSID)+"'"
    #for xy in zip(A,B):


    ymin=round(min(l7bot),-2)
    ymax=round(max(l1top),-1)
    #plt.yticks([ymin,ymax,0,-200,-400,-600,-800,-1000,-1500,-2000])
    plt.tight_layout()
    box = ax.get_position()
    ax.set_position([box.x0, box.y0+box.height*0.45, box.width, box.height*0.45])
    #the legend:
    p0 = Rectangle((0,0), 0.5, 0.5, fc = "w",fill=False, edgecolor='none', linewidth=0)
    p1 = Rectangle((0, 0), 1, 1, fc="khaki")
    p2 = Rectangle((0, 0), 1, 1, fc="olive")
    p3 = Rectangle((0, 0), 1, 1, fc="skyblue")
    p4 = Rectangle((0, 0), 1, 1, fc="saddlebrown")
    p5 = Rectangle((0, 0), 1, 1, fc="darkcyan")
    p6 = Rectangle((0, 0), 1, 1, fc="coral")
    p7 = Rectangle((0, 0), 1, 1, fc="mediumseagreen")
    l8 = matplotlib.lines.Line2D([], [], color='magenta', markersize=100)
    l9 = matplotlib.lines.Line2D([], [], color='cyan', markersize=100)
    l10 = matplotlib.lines.Line2D([], [], color='black', markersize=100)
    plt.legend([p0,p1, p2, p3, p4, p5, p6, p7,l8,l9,l10], 
               ["LEGEND","Layer 1","Layer 2","Layer 3","Layer 4","Layer 5","Layer 6","Layer 7",
                "2001 UFA Potentiometric Surface","2009 UFA Potentiometric Surface","Elevation of 10,000 mg/L TDS"],
               bbox_to_anchor=(0.6,-0.18),prop={'size':8}, fancybox=True,)
    plt.title(str(xsi))
    #location map
    im=plt.imread(get_sample_data(dir_XS+'/'+simnam+'_'+xsi+"_locmap.png"))
    ax1=fig.add_axes([0,0.05,0.35,0.35], anchor='S', zorder=1)
    ax1.imshow(im)
    ax1.axis('off')
    #ax1.annotate("Location Map", xy=(0.5, 1.05), xycoords='axes fraction', fontsize=6, verticalalignment='top', horizontalalignment='center')
    #plt.legend(loc="lower center", bbox_to_anchor=[0.5, 0],ncol=3, shadow=True, title="Legend", fancybox=True)
    plt.annotate("Figure # Cross Sections", xy=(3.5, 0.15), xycoords='axes fraction', fontsize=10, verticalalignment='bottom', horizontalalignment='right')
    plt.annotate(str(xsi), xy=(3.5, 0.05), xycoords='axes fraction', fontsize=10, verticalalignment='bottom', horizontalalignment='right')

    fig_file=dir_XS+"/"+str(xsi)+".png"
    plt.savefig(fig_file,dpi=300)
    #plt.show()
    plt.clf()
    plt.close()
    os.remove(dir_XS+'/'+simnam+'_'+xsi+"_locmap.png")

