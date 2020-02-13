% Program to store all CTs from the ADRC PET Dicoms
% Author: Mohammed Goryawala. Ph.D.
% Institution: University of Miami
% Date: 11/26/2019
%
% Modified - To Output T1 in Batch
% Author: Robin PM
% Institution: Florida International University
% Date: 02/12/2020
% Note:
% Adjusted for UM AIM data

clc
clear

%% Get all Patient Folders

% Parent folder with all batches or a single batch
parentFolder   = 'X:\RESEARCH\CATE_SHARE\CATE_Public\UM-Data\AIM_MRI';                %Modify to point to data location
dcm2niixFolder = 'C:\Users\RobinPM\Documents\temp_DCM2Nii\execs';       %Modify to point to dcm2niix location
curatedFolder  = 'X:\RESEARCH\CATE_SHARE\CATE_Public\UM-Data\Output';       %Output folder called 'CuratedFolder' 
mkdir(curatedFolder);

% Run through the folder to get all patient subfolders
list=dir(parentFolder);
list = list(~ismember({list.name},{'.','..'}));
dirFlags = [list.isdir];
subFolders = list(dirFlags);

for ii = 1:length(subFolders)
    k = strfind(subFolders(ii).name,'AIM-'); % Looks for the patient name starting with this Prefix to avoid running everything
    if (~isempty(k))
        if(k(1)==1)
            patientFolderCheck(ii) = ~isempty(k); % Avoids the presence of other '110' findings
        end
    end
end
patientFolderCheck = patientFolderCheck'; % Transpose for ease
patientFolders = subFolders(patientFolderCheck); % Keeps only patient folders

%% For each patient folder

for ii = 1:length(patientFolders)
    % Run the dcm2niix routine
    % This will convert all dicoms to NIFTI in the folder
    % Will also write a json file with parameters used to sort
    mkdir(fullfile(parentFolder,'tempExport'));
    command = [fullfile(dcm2niixFolder,'dcm2niix.exe') ...
        ' -t y -i y -o ',fullfile(parentFolder,'tempExport') , ' ',...
        '"', fullfile(patientFolders(ii).folder,patientFolders(ii).name),'"'];
    system(command);
    
    % Read all created json files
    jsons = dir(fullfile(parentFolder,'tempExport','*.json'));
    for jj = 1 : length(jsons)
        header = jsondecode(fileread(fullfile(jsons(jj).folder,jsons(jj).name)));
        
       % Filter to output the structural T1
        if(strcmp(header.Modality,'MR') && strcmp(header.MRAcquisitionType,'3D') && contains(upper(header.SeriesDescription), 'T1'))
             fprintf(header.Modality)
        fprintf(header.MRAcquisitionType)
        
            % Create Folder for each subject
            % Format is XXXXXX_YY_YY_YYYY where XXXXXX is the subject ID
            % and YY_YY_YYYY is the date of the scan
            % Scan date is derived from DICOM header for accuracy
            % JSON file has modality and the txt file has the scan date -- need
            % both for correctly getting folder names
            
            % Get Study Date
            [filepath,name,ext] = fileparts(fullfile(jsons(jj).folder,jsons(jj).name));
            a = importdata(fullfile(jsons(jj).folder,[name,'.txt'])); a = string(a{1});
            dateIndex = strfind(a,'DateTime');
            StudyDate = extractBetween(a,dateIndex+10,dateIndex+17);
            
            % Subject ID Maker - Change based on batch pattern
            nameLength = strlength(patientFolders(ii).name());
            if ( nameLength < 11)
                subID = convertStringsToChars(strcat(patientFolders(ii).name(1:nameLength),'_',StudyDate));
            else
                subID = convertStringsToChars(strcat(patientFolders(ii).name(1:11),'_',StudyDate));
            end
            
            % Create Folder
%             mkdir(fullfile(curatedFolder,subID));
            outFolder = fullfile(curatedFolder);
            
            % Move the CT Nifti File
            movefile(fullfile(jsons(jj).folder,[name,'.nii']),fullfile(outFolder,[subID,'.nii']));
        end
    end
     rmdir(fullfile(parentFolder,'tempExport'),'s');
end
