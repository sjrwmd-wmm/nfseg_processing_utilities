# Check the difference in output from original and modified versions


import numpy as np


#files_orig = ['WaterBodiesFromJohnGood.ufahds', 'WaterBodiesFromTrey.ufahds', 'WaterBodiesFromVito.ufahds']
#files_mod = ['WaterBodiesFromJohnGood_mod_layer_3.txt', 'WaterBodiesFromTrey_mod_layer_3.txt', 'WaterBodiesFromVito_mod_layer_3.txt']
files_orig = ['WaterBodiesFromTrey.ufahds', 'WaterBodiesFromVito.ufahds']
files_mod = ['WaterBodiesFromTrey_layer_3.txt','WaterBodiesFromVito_layer_3.txt']
#files_orig = ['WaterBodiesFromTrey.ufahds', 'WaterBodiesFromVito.ufahds']
#files_mod = ['WaterBodiesFromTrey_mod_layer_3.txt', 'WaterBodiesFromVito_mod_layer_3.txt']
#files_orig = ['WaterBodiesFromJohnGood.ufahds']
#files_mod = ['WaterBodiesFromJohnGood_mod_layer_3.txt']


n = len(files_orig)

# Threshold for values to be printed
threshold = np.float64(0) #np.float64(1e-9) #np.float64(1e-5) #np.float64(5e-6)

for i in range(n):
    
    print ('\n\nWorking on: {}\nOnly printing values greater than {}'.format(files_orig[i], threshold))
    
    odata_sp1 = {}
    odata_sp2 = {}
    mdata_sp1 = {}
    mdata_sp2 = {}
    
    # Read through each file separately in case files lengths are different
    with open(files_orig[i],'r') as forig:
        
        # Skip past the header lines
        forig.readline()
        
        # Go through the data lines
        for oline in forig:
            
            # Read whole line
            oline = oline.rstrip()
            
            #print (oline)
            # Get the lakeID as a string
            oID = oline.split()[0]
            
            # Get the original values
            ovalue_SP1 = np.float64(oline.split()[1])
            ovalue_SP2 = np.float64(oline.split()[2])
            
            
            # Update the data dictionaries
            odata_sp1.update({oID:ovalue_SP1})
            odata_sp2.update({oID:ovalue_SP2})
        #
    #
    
    with open(files_mod[i],'r') as fmod:
        
        # Skip past the header lines
        fmod.readline()
        
        # Go through the data lines
        for mline in fmod:
            
            # Read whole line
            mline = mline.rstrip()
            
            #print(mline)
            mID = mline.split()[0]
            
            # Get the modified values
            mvalue_SP1 = np.float64(mline.split()[1])
            mvalue_SP2 = np.float64(mline.split()[2])
            
            
            # Update the data dictionaries
            mdata_sp1.update({mID:mvalue_SP1})
            mdata_sp2.update({mID:mvalue_SP2})
        #
    #
    #print (len(mdata_sp1),len(odata_sp1))
    
    # Output the differences to a csv file
    foutput = '{}_diff_from_original.csv'.format('.'.join(files_mod[i].split('.')[:-1]))
    
    # Determine the largest number of keys between original and modified
    if (len(odata_sp1)>=len(mdata_sp1)):
        keys = list(odata_sp1.keys())
    elif (len(odata_sp1)<len(mdata_sp1)):
        keys = list(mdata_sp1.keys())
    #
    
    # Find the differences
    with open(foutput,'w') as fout:
        
        fout.write ('LakeID,diff_SP1,diff_SP2\n')
        
        missingkeys = []
        
        for key in keys:
            # Calculate the difference and print to screen
            try:
                diff_SP1 = mdata_sp1[key] - odata_sp1[key]
                diff_SP2 = mdata_sp2[key] - odata_sp2[key]
            except KeyError:
                #fout.write ('Key in original but missing in modified: {}\n'.format(key))
                missingkeys.append(key)
            else:
                if (np.abs(diff_SP1)>=threshold or np.abs(diff_SP2)>=threshold):
                    fout.write ('{},{},{}\n'.format(key,diff_SP1,diff_SP2))
            #
        #
        
        # Now write out the missing keys
        fout.write('\n\nMissing Keys:\n')
        fout.write('LakeID,Original_SP1,OriginalSP2,New_SP1,New_SP2\n')
        for key in missingkeys:
            if key not in mdata_sp1:
                fout.write('{},{},{},,\n'.format(key,odata_sp1[key],odata_sp2[key]))
            elif key not in odata_sp1:
                fout.write('{},,,{},{}\n'.format(key,mdata_sp1[key],mdata_sp2[key]))
            else:
                fout.write('{},{},{},{},{}\n'.format(key,odata_sp1[key],odata_sp2[key],mdata_sp1[key],mdata_sp2[key]))
    #
#
