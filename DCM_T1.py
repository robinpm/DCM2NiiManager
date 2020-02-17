# Pseudocode:
# Make list of folders NOT DONE
# take first folders
# make list of files in folder WORKING
# run pydicom to read header, check for modality 3d and other flags
# return correct file to array, process nifti(how)
# repeat on next folder
#
# To improve: not scour every single file, find one and process 
#             other to check if attribute is present  
import os
import shutil
from pydicom import dcmread
import time



# Set up directory where DICOM folders are
workDir = "X:\\RESEARCH\\CATE_SHARE\\CATE_Public\\UM-Data\\AIM_MRI\\8-00461_8-00461_MR_2018-01-18_174143_Research^DetectPAD.2015-01_t1.mprage.sag.p2.iso.1mm_n192__00000\\" #to be changed
exeDir = "C:\\Users\\RobinPM\\Documents\\gits\\DICOM_Nii_T1\\execs\\" #to be changed


os.chdir(workDir) # Points to user directory
dcmList = os.listdir() # Makes list of files wi

start = time.perf_counter()
t1Arr = [] # Create Array of found T1s

os.mkdir(workDir + '\\temps')



for i in range (0, len(dcmList)):
    print(dcmList[i])
    fPath = (workDir + dcmList[i]) # Get Full Path for dicom
    
    if(('.dcm' in fPath) or not ('.' in fPath)):
        currentHead = dcmread(fPath) # Get header from dicom
        # print(currentHead)
        # testo = (str(currentHead).find("MR Acquisition Type")) # Check to find label in header'
        if (hasattr(currentHead,'MRAcquisitionType')) and (currentHead.Modality == 'MR') and (currentHead.MRAcquisitionType =='3D') and ((str.upper(currentHead.SeriesDescription)).find('T1') > -1):
            # print( dcmList[i])
            t1Arr.append(dcmList[i])
            shutil.copyfile((workDir + dcmList[i]),(workDir+'temps\\'+dcmList[i]))
# os.mkdir('out1')
print(workDir)
os.system(exeDir + 'dcm2niix.exe -o '+ workDir + 'out1\\ ' + workDir + 'temps\\')
# shutil.rmtree('./temp/')

print(str(round(time.perf_counter() - start, 2)))
# os.mkdir('out2')
os.system(exeDir + 'dcm2niix.exe -o '+ workDir + 'out2\\ ' + workDir)


print(len(t1Arr))
print(len(dcmList))
os.system