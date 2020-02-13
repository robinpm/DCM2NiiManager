# Pseudocode:
# Make list of folders NOT DONE
# take first folders
# make list of files in folder WORKING
# run pydicom to read header, check for modality 3d and other flags
# return correct file to array, process nifti(how)
# repeat on next folder

import os
import dicom2

# Set up directory where DICOM folders are
workDir = "C:\\Users\\RobinPM\\Documents\\gits\\DICOM_Nii_T1\\scans\\AIM-00502\\" #to be changed


os.chdir(workDir) # Points to user directory
dcmList = os.listdir() # Makes list of files wi
