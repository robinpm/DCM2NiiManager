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
from datetime import date
from tqdm import tqdm as pb
import logging

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',filename='run.log',level=logging.DEBUG,datefmt='%Y-%m-%d %H:%M:%S')

parentDir = "X:\\RESEARCH\\CATE_SHARE\\CATE_Public\\UM-Data\\AIM_MRI\\"

logging.info( "Parent Directory is:\n" + str(parentDir))
os.chdir(parentDir)
folderList = os.listdir()  # Makes list of files wi
logging.info(str(date.fromtimestamp(time.time()))+ " List of Files Found:\n" + str(folderList))

for fIn in pb( range(0, len(folderList))):

        # Set up directory where DICOM folders are
    workDir = parentDir + folderList[fIn] + '\\' # to be changed
    exeDir = "C:\\Users\\RobinPM\\Documents\\gits\\DICOM_Nii_T1\\execs\\"  # to be changed
    logging.info( "currently processing " +  str(folderList[fIn]))

    winPath = workDir

    if ('^' in workDir):
        winPath = winPath.replace('^', '^^')
        logging.error('The folder name had an invalid character, changing name to:\n' + winPath)

    os.chdir(workDir)  # Points to user directory

    dcmList = os.listdir()  # Makes list of files wi

    start = time.perf_counter()
    t1Arr = []  # Create Array of found T1s
    tempDir = (workDir + 'temps\\')
    if (os.path.isfile(tempDir)):
        os.mkdir(tempDir)
        for i in pb( range(0, len(dcmList))):
            # print(dcmList[i])
            fPath = (workDir + dcmList[i])  # Get Full Path for dicom

            if(('.dcm' in fPath) or not ('.' in fPath)):
                currentHead = dcmread(fPath)  # Get header from dicom
                # print(currentHead)
                # testo = (str(currentHead).find("MR Acquisition Type")) # Check to find label in header'
                if (hasattr(currentHead, 'MRAcquisitionType')) and (currentHead.Modality == 'MR') and (currentHead.MRAcquisitionType == '3D') and ((str.upper(currentHead.SeriesDescription)).find('T1') > -1):
                    # print( dcmList[i])
                    t1Arr.append(dcmList[i])
                    shutil.copyfile(
                        (workDir + dcmList[i]), (workDir+'temps\\'+dcmList[i]))
        os.mkdir('out1')
        os.system(exeDir + 'dcm2niix.exe -o ' + winPath +
                'out1\\ ' + winPath + 'temps\\')
        # shutil.rmtree('./temp/')

        logging.info(folderList[fIn] + " took " + str(round(time.perf_counter() - start, 2)) + " seconds to run")
        # # os.mkdir('out2')
        # os.system(exeDir + 'dcm2niix.exe -o ' + winPath + 'out2\\ ' + winPath)
    else:
        logging.error( "Folder Temp already exists for " + str(folderList[fIn]))



