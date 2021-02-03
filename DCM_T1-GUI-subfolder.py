# Pseudocode:
# Make list of folders done
# take first folders done
# make list of files in folder done
# run dcm2niftii to read header, check for modality 3d and other flags
# return correct file to array, process nifti(how)
# repeat on next folder
#
# To improve: Add Create function for folder traversal --> implement recursive method for subfolders
#              not scour every single file, find one and process
#             other to check if attribute is present
#             dcm2niftii has flag to run only one series, next big step ALERT ALERT
# 
# to think of: include blacklisted character to ease window processing i.e. " " "^"
# Find case when it finds unexpected files or folders
# check output folder to see if it outputed the right file as a way to doublecheck
# 

from tkinter import *
from tkinter import filedialog as fd 
import tkinter as tk
from tkinter.ttk import *
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
global nSource
global nSeries


logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',filename='run.log',level=logging.DEBUG,datefmt='%Y-%m-%d %H:%M:%S')
print(os.path.dirname(os.path.realpath(sys.path[0])))

# GUI WINDOW
def callback():
    global name
    name = fd.askdirectory() 

#Creating GUI Window
root = Tk()
def applyVar():
    global source_name
    global series_name 
    source_name = soName.get()
    series_name = seName.get()
    root.destroy
#progress = Progressbar(root,orient=HORIZONTAL,length=100, mode= 'indeterminate')


root.geometry("400x300")
Label(root, text="Enter Source Name").pack()
soName = Entry(root)
soName.pack()

Label(root, text="Enter Series Name").pack()
seName = Entry(root)
seName.pack()

tk.Button(text='Select Import Directory', command=callback).pack(pady=20)
tk.Button(text='Apply', command=applyVar).pack(pady=20)

root.mainloop()
# End Window GUI
nSeries = series_name
nSource = source_name

# series_name = sName.get()
print("series Selected: " + series_name)

try: name
except NameError:
    print("No directory indicated\nQuitting...")
else:
    print("Director is:" + name)
    


parentDir = Path(name)
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

    if ('^' in str(workDir)):
       winPath = str(winPath).replace('^', '^^')
       logging.error('The folder name had an invalid character, changing name to:\n' + winPath)

    os.chdir(workDir)  # Points to user directory

    dcmList = os.listdir()  # Makes list of files wi

    #subfolder case
    sfileCount = len(dcmList)
    if (sfileCount < 100):
        subList = dcmList
        for sfIn in pb( range(0, len(subList))):

            sworkDir = Path.joinpath(workDir, subList[sfIn]) # to be changed
            #logging.info( "currently processing " +  str(folderList[fIn]))
            os.chdir(sworkDir)
            winPath = sworkDir
            sdcmList = os.listdir()

            start = time.perf_counter()
            t1Arr = []  # Create Array of found T1s
            tempDir = Path.joinpath(sworkDir, 'PT/')
            if (not os.path.exists(tempDir)):
                os.mkdir(tempDir)
                for i in pb( range(0, len(sdcmList))):
                    # print(dcmList[i])
                    sfPath = Path.joinpath(sworkDir , sdcmList[i])  # Get Full Path for dicom

                    if(('.dcm' in str(sfPath)) or not ('.' in str(sfPath))):
                        currentHead = dcmread(str(sfPath))  # Get header from dicom
                        # print(currentHead)
                        # testo = (str(currentHead).find("MR Acquisition Type")) # Check to find label in header'
                        if (currentHead.Modality == 'PT'): #(hasattr(currentHead, 'MRAcquisitionType')) and (currentHead.Modality == 'PT') and (currentHead.MRAcquisitionType == '3D') and ((str.upper(currentHead.SeriesDescription)).find('T1') > -1):
                            # print( dcmList[i])
                            t1Arr.append(sdcmList[i])
                            print((str(workDir) + sdcmList[i]))
                            shutil.copyfile((str(sworkDir) + "/" + sdcmList[i]), (str(sworkDir)+'/PT/'+sdcmList[i]))

                os.mkdir('Niftii')
                fName = str(winPath)[-6:-1]
                nDate   = (datetime.now()).strftime("%Y%m%d%H%M%S")
                pID = str(winPath)[78:84]
                #print(pID) 
                os.system(str(exeDir) + "/dcm2niix.exe -f " + nSource + "-" + nSeries + "-" + pID + "-%t-" +str(nDate) + ' -o ' + str(winPath) + '\\Niftii\\ ' + str(winPath) + "/PT")
                # shutil.rmtree('./temp/')

                logging.info(folderList[fIn] + " took " + str(round(time.perf_counter() - start, 2)) + " seconds to run")
                # # os.mkdir('out2')
                # os.system(exeDir + 'dcm2niix.exe -o ' + winPath + 'out2\\ ' + winPath)
            else:
                logging.error( "Folder Temp already exists for " + str(folderList[fIn]))
            
    else:
        start = time.perf_counter()
        t1Arr = []  # Create Array of found T1s
        tempDir = Path.joinpath(workDir, 'PT/')
        if (not os.path.exists(tempDir)):
            os.mkdir(tempDir)
            for i in pb( range(0, len(dcmList))):
                # print(dcmList[i])
                fPath = Path.joinpath(workDir , dcmList[i])  # Get Full Path for dicom

                if(('.dcm' in str(fPath)) or not ('.' in str(fPath))):
                    currentHead = dcmread(str(fPath))  # Get header from dicom
                    # print(currentHead)
                    # testo = (str(currentHead).find("MR Acquisition Type")) # Check to find label in header'
                    if (currentHead.Modality == 'PT'): #(hasattr(currentHead, 'MRAcquisitionType')) and (currentHead.Modality == 'PT') and (currentHead.MRAcquisitionType == '3D') and ((str.upper(currentHead.SeriesDescription)).find('T1') > -1):
                        # print( dcmList[i])
                        t1Arr.append(dcmList[i])
                        print((str(workDir) + dcmList[i]))
                        shutil.copyfile((str(workDir) + "/" + dcmList[i]), (str(workDir)+'/PT/'+dcmList[i]))

            os.mkdir('Niftii')
            fName = str(winPath)[-6:-1]
            nDate   = (datetime.now()).strftime("%Y%m%d%H%M%S")
            pID = str(winPath)[78:84]
            #print(pID) 
            os.system(str(exeDir) + "\\dcm2niix.exe -f " + nSource + "-" + nSeries + "-" + pID + "-%t-" +str(nDate) + ' -o ' + str(winPath) + '\\Niftii\\ ' + str(winPath) + "/PT")
            # shutil.rmtree('./temp/')

            logging.info(folderList[fIn] + " took " + str(round(time.perf_counter() - start, 2)) + " seconds to run")
            # # os.mkdir('out2')
            # os.system(exeDir + 'dcm2niix.exe -o ' + winPath + 'out2\\ ' + winPath)
        else:
            logging.error( "Folder Temp already exists for " + str(folderList[fIn]))




