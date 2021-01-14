# Pseudocode:
# Make list of folders done
# take first folders done
# make list of files in folder done
# run dcm2niftii to read header, check for modality 3d and other flags
# return correct file to array, process nifti(how)
# repeat on next folder
#
# To improve: not scour every single file, find one and process
#             other to check if attribute is present
#             dcm2niftii has flag to run only one series, next big step ALERT ALERT
# 
# to think of: include blacklisted character to ease window processing i.e. " " "^"
# Find case when it finds unexpected files or folders
# check output folder to see if it outputed the right file as a way to doublecheck
# 
import os
import sys
import shutil
from pydicom import dcmread
import time
from datetime import datetime
from tqdm import tqdm as pb
import logging
from pathlib import Path

# Global Vars
# source-series-rid_petdate_reg_rid_mridate-processingdate
nSource = "MTS"
nSeries = "110"
nDate   = datetime.now().strftime("%D%M%Y%H%M%S")

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',filename='run.log',level=logging.DEBUG,datefmt='%Y-%m-%d %H:%M:%S')
print(os.path.dirname(os.path.realpath(sys.path[0])))
parentDir = Path("X:/RESEARCH/CATE_SHARE/CATE_Public/NWSI-Site_Data/MtSinai-Data/PET/batch1/DCM-test")
exeDir = Path("C:/Users/RobinPM/Documents/gits/DICOM_Nii_T1/execs")

logging.info( "Parent Directory is:\n" + str(parentDir))
os.chdir(parentDir)
folderList = os.listdir()  # Makes list of files wi
logging.info(str(datetime.fromtimestamp(time.time()))+ " List of Files Found:\n" + str(folderList))

for fIn in pb( range(0, len(folderList))):

        # Set up directory where DICOM folders are
    workDir = Path.joinpath(parentDir, folderList[fIn]) # to be changed
    logging.info( "currently processing " +  str(folderList[fIn]))

    winPath = workDir

    # if (' ' in workDir):
    #     winPath = winPath.replace(' ', '_')
    #     logging.error('The folder name had an invalid character, changing name to:\n' + winPath)

    #if ('^' in workDir):
    #    winPath = winPath.replace('^', '^^')
    #   logging.error('The folder name had an invalid character, changing name to:\n' + winPath)

    os.chdir(workDir)  # Points to user directory

    dcmList = os.listdir()  # Makes list of files wi

    start = time.perf_counter()
    t1Arr = []  # Create Array of found T1s
    tempDir = Path.joinpath(workDir, 'temps/')
    if (not os.path.exists(tempDir)):
        # os.mkdir(tempDir)
        # for i in pb( range(0, len(dcmList))):
        #     # print(dcmList[i])
        #     fPath = (workDir + dcmList[i])  # Get Full Path for dicom

        #     if(('.dcm' in fPath) or not ('.' in fPath)):
        #         currentHead = dcmread(fPath)  # Get header from dicom
        #         # print(currentHead)
        #         # testo = (str(currentHead).find("MR Acquisition Type")) # Check to find label in header'
        #         if (hasattr(currentHead, 'MRAcquisitionType')) and (currentHead.Modality == 'MR') and (currentHead.MRAcquisitionType == '3D') and ((str.upper(currentHead.SeriesDescription)).find('T1') > -1):
        #             # print( dcmList[i])
        #             t1Arr.append(dcmList[i])
        #             shutil.copyfile(
        #                 (workDir + dcmList[i]), (workDir+'temps\\'+dcmList[i]))
        os.mkdir('out1')
        fName = str(winPath)[-6:-1]
        os.system(str(exeDir) + "\\dcm2niix.exe -f " + nSource + "-" nSeries + "-%i-%t" + nDate + ' -o ' + str(winPath) + '\\out1\\ ' + str(winPath) + "\\")
        # shutil.rmtree('./temp/')

        logging.info(folderList[fIn] + " took " + str(round(time.perf_counter() - start, 2)) + " seconds to run")
        # # os.mkdir('out2')
        # os.system(exeDir + 'dcm2niix.exe -o ' + winPath + 'out2\\ ' + winPath)
    else:
        logging.error( "Folder Temp already exists for " + str(folderList[fIn]))




