# Activity_Viewer
Interactive Graphical User Interface (GUI) That allows you to manually draw ROIs and extract activity from 2-photon imaging videos. 

Created by William (Jake) Wright

## Getting Started
To launch the GUI simply type Activity_Viewer in the command line terminal of anaconda prompt. Can also launch the GUI by running the main() function in Activity_Viewer_pyqt.py

Upon opening the GUI load a reference image. This can be a single tif image or a tif stack time series. This reference image will be used for drawing the ROIs. 

After drawing ROIs, extract the traces. You will be prompted to select the directory where your time series images are located. Raw fluorescence is then extracted and a new window will popup. This will allow you to inspect the traces and specify any further processing you wish you perform. After processing, a final window will popup for inspecting the final outputs which can be saved in a dataclass. 

## Functionality

### ROI Drawing
From the main menu bar
- File
    - Open Image - opens reference image
    - Load ROIs - loads ROIs previously drawn and saved
    - Save ROIs - save current ROIs to use later
    - New Session - no current function
    - Exit - Closes the GUI
- Image
    - Color Map - change the color map of the reference image from the given options
    - Display Options - change how the reference iamge is being displayed if a video. Can be shown as a video, max, or average projections
    - Aspect Ratio - choose the aspect ratio of the reference image to be fixed or fit the window
- ROIs
    -Color - allows you to select the color of the drawn rois

Draw ROIs section
    - Background - Draw a single ROI to caputure the background
    - Dendrite - Draw series of ROIs along the length of dendrite that are held together in a container
    - Spine - Draw individual ROIs for dendritic spines
    - Soma - Draw individual ROIs for cell somas

Manage ROIs section
    - Select ROIs - allows for ROI selection
    - Shift ROIs - allows for shifting all ROIs together at once
    - Label ROIs - toggles the ROIs labels
    - Flag ROIs - add flags to ROIs (e.g. new spine)
    - Delete ROIs - select and delete ROIs
    - Clear ROIs - deletes all ROIs 
    - Save ROIs - saves ROIs to for later use
    - Extract Traces - extract fluorescence traces from tif images

Parameters
    - Imaging Sensor - select imaging sensor used
    - Zoom Value - specify the digital zoom value used (this is specifically for BScope with 16x Nikon objective)
    - Imaging Rate - imaging rate used

### Processing Window
Parameters
    - Calculate dFoF - to calculate dFoF
    - Deconvolve Trace - to deconvolve to estimate spikes
    - Calculate Volume - to calculate spine volume (spines only)
    - Correct Bout Separations - to correct separations between imaging bouts or not
    - Smooth Window - time frame (s) to smooth trace over for the processed dFoF
    - Artifact Frames - specify frames to be ignored due to artifacts
    - Dendrite Grouping - specify which spines belong to which dendrites

ROIs
    - Select ROIs to display their raw fluorescence traces in the plot

Process
    - Triggers further processing

### Output Window
Display Data
    - Select what data you wish to display in the plots

ROIs
    - Select ROIs to display their data in the plosts

Save
    - Save the final output

