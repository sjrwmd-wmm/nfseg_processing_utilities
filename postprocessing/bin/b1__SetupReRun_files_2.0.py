import arcpy
import sys
import os
import shutil
import time
arcpy.env.overwriteOutput = True
start = time.clock()

BIN_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0,BIN_DIR)
#PATH = (os.getcwd() + "\\" + "bin")
#sys.path.insert(0,PATH)

import my_utilities_NFSEG as myut


reffile_dir = sys.argv[1]

# Get the working PATHs
cpath_py, cpath_py_upper, cpath_py_base = myut.get_current_PATHs()


# Print the results to screen
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


# Follow steps from "Instructions from Wei.pdf"
#create a folder starting with 'water_bduget_'
if os.path.isdir(cpath_py+'/rerunCBB/water_budget_rerun') is True:
    print ("rerun folder already created - files will be overwritten")
else:
    if os.path.isdir(cpath_py+'/rerunCBB') is True:
        os.mkdir(cpath_py+'/rerunCBB/water_budget_rerun')
    else:
        os.mkdir(cpath_py+'/rerunCBB')
        os.mkdir(cpath_py+'/rerunCBB/water_budget_rerun')
dir_rerun = cpath_py+'/rerunCBB/water_budget_rerun'

# Copy files over that are needed to run the Water Budget executables
filecopylist = ['mfnwt_nfseg_all_to_cbc.in',
                'nfseg.springs.csv',
                'NFSEG_2001_WaterBudgetAnalysis.xlsm',
                'NFSEG_2009_WaterBudgetAnalysis.xlsm',
                'nfseg_all_to_cbc.chd',
                'nfseg_all_to_cbc.nam',
                'nfseg_all_to_cbc.nwt',
                'nfseg_all_to_cbc.oc',
                'nfseg_all_to_cbc_sh.hds']
for f in filecopylist:
    shutil.copy2(os.path.join(reffile_dir,f), os.path.join(dir_rerun,f))
#


#Step 2a - part one from active simulation
#copy files from latest simulation folder into water_budget subfolder - No name change
sim_files=["recharge_mul_2009.ref","evt_rate_after_mul_2001.ref","evt_rate_after_mul_2009.ref",
          "kx1.ref","kx2.ref","kx3.ref","kx4.ref","kx5.ref","kx6.ref","kx7.ref","kz1.ref",
          "kz2.ref","kz3.ref","kz4.ref","kz5.ref","kz6.ref","kz7.ref","recharge_mul_2001.ref",
           "gwv_springs_conductances.dat",
           "ibound1.inf","ibound2.inf","ibound3.inf","ibound4.inf","ibound5.inf","ibound6.inf","ibound7.inf"]
for file in sim_files:
    if os.path.isfile(cpath_py_upper+'/'+file) is False:
        print("missing file: "+ cpath_py_upper + '/ '+ file)
    else:
        shutil.copy2(cpath_py_upper+'/'+file,dir_rerun+'/'+file)

#copy files from Wei's Water Budget setup folder into current water_budget subfolder - No name change
templ_files=["mfnwt_nfseg_all_to_cbc.in","nfseg_all_to_cbc.nam","nfseg_all_to_cbc.chd",
             "nfseg_all_to_cbc.oc","nfseg_all_to_cbc.nwt","nfseg.springs.csv",
             "NFSEG_2001_WaterBudgetAnalysis.xlsm","NFSEG_2009_WaterBudgetAnalysis.xlsm"]
dir_templ = cpath_py+'/rerunCBB/background/water_budget'
for file in templ_files:
    if os.path.isfile(dir_templ+'/'+file) is False:
        print("missing file: "+ dir_templ + '/' + file)
    else:
        shutil.copy2(dir_templ+'/'+file,dir_rerun+'/'+file)

#copy files from latest simulation folder into water_budget subfolder - Rename for *.nam file
renamed_files=["nfseg.bas","nfseg.dis"]
for file in renamed_files:
    if os.path.isfile(cpath_py_upper+'/'+file) is False:
        print("missing file: " + cpath_py_upper + '/' + file)
    else:
        shutil.copy2(cpath_py_upper+'/'+file,dir_rerun+'/'+file[:-4]+"_all_to_cbc"+file[-4:])

renamed_files2=["nfseg.zone"]
for file in renamed_files2:
    if os.path.isfile(cpath_py_upper+'/'+file) is False:
        print("missing file: " + cpath_py_upper + '/' + file)
    else:
        shutil.copy2(cpath_py_upper+'/'+file,dir_rerun+'/'+file[:-5]+"_all_to_cbc"+file[-5:])

#Step 2b - copy from simdir then CHANGE THESE FILES copy drn, riv, and ghb files ; 
###change the 3rd line -50 with 50
bc_files = ["nfseg.drn","nfseg.riv","nfseg.ghb"]
for file in bc_files:
    print("updating ",file," to all_to_cbc version")
    if os.path.isfile(cpath_py_upper+'/'+file) is False:
        print("missing file: " + cpath_py_upper + '/' + file)
    else:
        with open(cpath_py_upper+'/'+file,mode='r') as inp:
            inplines=inp.readlines()
        #print inplines[0]
        #print inplines[1]
        newfile="nfseg_all_to_cbc"+file[-4:]
        print(newfile)
        with open(dir_rerun+'/'+newfile,mode='w') as out:
            lc=-1
            for line in inplines:
                lc=lc+1
                if lc==2:
                    line = line.replace("-50"," 50")
                out.write(line)

upw_files = ["nfseg.upw"]
for file in upw_files:
    print("updating ",file," to all_to_cbc version")
    if os.path.isfile(cpath_py_upper+'/'+file) is False:
        print("missing file: " + cpath_py_upper + '/' + file)
    else:
        with open(cpath_py_upper+'/'+file,mode='r') as inp:
            inplines=inp.readlines()
        #print inplines[0]
        #print inplines[1]
        newfile="nfseg_all_to_cbc"+file[-4:]
        print(newfile)
        with open(dir_rerun+'/'+newfile,mode='w') as out:
            lc=-1
            for line in inplines:
                lc=lc+1
                if lc==1:
                    items=line.split()
                    #print items
                    line=" 50  -1.000000e+030 0 0"+'\n'
                out.write(line)


mnw2_files = ["nfseg.mnw2"]
for file in mnw2_files:
    print("updating ",file," to all_to_cbc version")
    if os.path.isfile(cpath_py_upper+'/'+file) is False:
        print("missing file: " + cpath_py_upper + '/' + file)
    else:
        with open(cpath_py_upper+'/'+file,mode='r') as inp:
            inplines=inp.readlines()
        #print inplines[0]
        #print inplines[1]
        newfile="nfseg_all_to_cbc"+file[-5:]
        print(newfile)
        with open(dir_rerun+'/'+newfile,mode='w') as out:
            lc=-1
            for line in inplines:
                lc=lc+1
                if lc==0:
                    items=line.split()
                    #print items
                    line='{0:>4}'.format(items[0])
                    line=line+'{0:>3}'.format("50")
                    line=line+'{0:>4}'.format("0")+'\n'
                out.write(line)

wel_files = ["nfseg.wel"]
for file in wel_files:
    print("updating ",file," to all_to_cbc version")
    if os.path.isfile(cpath_py_upper+'/'+file) is False:
        print("missing file: " + cpath_py_upper + '/' + file)
    else:
        with open(cpath_py_upper+'/'+file,mode='r') as inp:
            inplines=inp.readlines()
        #print inplines[0]
        #print inplines[1]
        newfile="nfseg_all_to_cbc"+file[-4:]
        print(newfile)
        with open(dir_rerun+'/'+newfile,mode='w') as out:
            lc=-1
            for line in inplines:
                lc=lc+1
                if lc==1:
                    items=line.split()
                    #print items
                    line='{0:>10}'.format(items[0])
                    line=line+'{0:>10}'.format("50")+'\n'
                out.write(line)

rchet_files = ["nfseg.evt","nfseg.rch"]
for file in rchet_files:
    print("updating ",file," to all_to_cbc version")
    if os.path.isfile(cpath_py_upper+'/'+file) is False:
        print("missing file: " + cpath_py_upper + '/' + file)
    else:
        with open(cpath_py_upper+'/'+file,mode='r') as inp:
            inplines=inp.readlines()
        #print inplines[0]
        #print inplines[1]
        newfile="nfseg_all_to_cbc"+file[-4:]
        print(newfile)
        with open(dir_rerun+'/'+newfile,mode='w') as out:
            lc=-1
            for line in inplines:
                lc=lc+1
                if lc==2:
                    items=line.split()
                    #print items
                    line='{0:>2}'.format(items[0])
                    line=line+'{0:>3}'.format("50")+'\n'
                out.write(line)

strthds_files = ["nfseg_sh.hds"]
for file in strthds_files:
    print("updating ",file," to all_to_cbc version")
    if os.path.isfile(cpath_py_upper+'/'+file) is False:
        print("missing file: " + cpath_py_upper + '/' + file)
    else:
        with open(cpath_py_upper+'/'+file,mode='r') as inp:
            inplines=inp.readlines()
        #print inplines[0]
        #print inplines[1]
        newfile="nfseg_all_to_cbc_sh.hds"
        shutil.copy2(cpath_py_upper+'/'+file,dir_rerun+'/'+newfile)
        print(newfile)








stop = time.clock()
DUR=round((stop-start)/60,1)
print("Script b1 completed in "+str(DUR)+" min")


