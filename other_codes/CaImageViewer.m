function varargout = CaImageViewer(varargin)
% CAIMAGEVIEWER MATLAB code for CaImageViewer.fig
%      CAIMAGEVIEWER, by itself, creates a new CAIMAGEVIEWER or raises the existing
%      singleton*.
%
%      H = CAIMAGEVIEWER returns the handle to a new CAIMAGEVIEWER or the handle to
%      the existing singleton*.
%
%      CAIMAGEVIEWER('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in CAIMAGEVIEWER.M with the given input arguments.
%
%      CAIMAGEVIEWER('Property','Value',...) creates a new CAIMAGEVIEWER or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before CaImageViewer_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to CaImageViewer_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help CaImageViewer

% Last Modified by GUIDE v2.5 08-Oct-2018 17:07:25

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @CaImageViewer_OpeningFcn, ...
                   'gui_OutputFcn',  @CaImageViewer_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before CaImageViewer is made visible.
function CaImageViewer_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to CaImageViewer (see VARARGIN)

% Choose default command line output for CaImageViewer
global gui_CaImageViewer
global zStack_Interface

handles.output = hObject;

gui_CaImageViewer.figure.handles = handles;

Users = {'Nathan', 'Yessenia', 'Sayyed', 'Jake', 'Other'}; 

Scrsz = get(0, 'Screensize');
    dialogboxwidth = 315;
    dialogboxheight = 150;
    d = dialog('Position', [(Scrsz(3)/2)-dialogboxwidth/2 Scrsz(4)/2-dialogboxheight/2 dialogboxwidth dialogboxheight ], 'Name', 'User');
    txt = uicontrol('Parent', d, 'Style', 'text', 'Position', [15 100 270 30], 'String', 'Select User:');
    
    btnspacing = 0.5;
    edgemargin = 15;
    btnwidth = (dialogboxwidth-2*edgemargin-((length(Users)-1)*btnspacing))/length(Users);
    
    for i = 1:length(Users)
        btn{i} = uicontrol('Parent', d, 'Style', 'pushbutton', 'Position', [edgemargin+((i-1)*btnwidth)+((i-1)*btnspacing) 30 btnwidth 25], 'String', Users{i}, 'Callback', @DlgChoice);
    end    
    uiwait(d)
    choice = get(d, 'UserData');
    if strcmpi(choice, 'Other')
        id = inputdlg('Enter user name:', 'New User', 1);
        set(handles.figure1, 'UserData', id{1})
    else
        set(gui_CaImageViewer.figure.handles.figure1, 'UserData', choice);
    end
    delete(d);


% Update handles structure
guidata(hObject, handles);
zStack_Interface.figure = [];

%%% Set appearance of GUI
set(handles.GreenGraph, 'YTick', []);
set(handles.GreenGraph, 'XTick', []);
set(handles.GreenGraph, 'Box', 'on');
set(handles.RedGraph, 'YTick', []);
set(handles.RedGraph, 'XTick', []);
set(handles.RedGraph, 'Box', 'on');
linkaxes([handles.GreenGraph, handles.RedGraph], 'xy')


%%% Initialize Key press functions for various editable text boxes
set(gui_CaImageViewer.figure.handles.Frame_EditableText, 'KeyPressFcn', @frameset);
set(gui_CaImageViewer.figure.handles.UpperLUT_EditableText, 'KeyPressFcn', @frameset);
set(gui_CaImageViewer.figure.handles.RedUpperLUT_EditableText, 'KeyPressFcn', @frameset);
set(gui_CaImageViewer.figure.handles.LowerLUT_EditableText, 'KeyPressFcn', @frameset);
set(gui_CaImageViewer.figure.handles.RedLowerLUT_EditableText, 'KeyPressFcn', @frameset);
set(gui_CaImageViewer.figure.handles.SmoothingFactor_EditableText, 'KeyPressFcn', @frameset);
set(gui_CaImageViewer.figure.handles.GreenGamma_EditableText, 'KeyPressFcn', @frameset);
set(gui_CaImageViewer.figure.handles.RedGamma_EditableText, 'KeyPressFcn', @frameset);
set(gui_CaImageViewer.figure.handles.figure1, 'KeyPressFcn', @ImageSlider_Slider_Callback)


%%% Initialize Various Parameters
gui_CaImageViewer.CurrentCMap = 'RGB';
gui_CaImageViewer.NewSpineAnalysis = 0;
gui_CaImageViewer.NewSpineAnalysisInfo.CurrentDate = [];
gui_CaImageViewer.NewSpineAnalysisInfo.CurrentImagingField = [];
gui_CaImageViewer.NewSpineAnalysisInfo.SpineList = [];
set(handles.Autoscale_CheckBox, 'Value', 1);
set(handles.Merge_ToggleButton, 'Enable', 'off');


%%%%% Clear All ROIs and Associated Labels %%%%%%

% clearROIs = findobj('Type', 'rectangle');
% for i = 1:length(clearROIs);
%     delete(clearROIs(i));
% end
% clearTexts = findobj('Type', 'Text');
% 
% clearLines = findobj('Type', 'Line');
% delete(clearLines)
    
gui_CaImageViewer.ROI = [];
gui_CaImageViewer.ROIother = [];
gui_CaImageViewer.ROItext = [];
gui_CaImageViewer.PolyROI = [];
gui_CaImageViewer.PolyLinePos = [];
gui_CaImageViewer.PolyLineVertices = [];
gui_CaImageViewer.Spine_Number = 0;
gui_CaImageViewer.Dendrite_Number = 0;
gui_CaImageViewer.DendritePolyPointNumber = [];
gui_CaImageViewer.SpineDendriteGrouping = [];
gui_CaImageViewer.Dendrite_ROIs = 0;
gui_CaImageViewer.LoadedFile = 0;
gui_CaImageViewer.filename = [];
gui_CaImageViewer.GCaMP_Image = [];
gui_CaImageViewer.Red_Image = [];
gui_CaImageViewer.ch1image = [];
gui_CaImageViewer.imageserieslength = [];
gui_CaImageViewer.UsingSurroundBackground = 0; 
gui_CaImageViewer.SurroundBackgroundBuffer = 5;
gui_CaImageViewer.BackgroundROI = [];

gui_CaImageViewer.GreenGraph_loc = get(handles.GreenGraph, 'Position');
gui_CaImageViewer.RedGraph_loc = get(handles.RedGraph, 'Position');

function DlgChoice(hObject, eventdata, ~)

button = get(hObject);

choice = button.String;

sourcewindow = button.Parent;

set(sourcewindow, 'UserData', choice);

uiresume


% UIWAIT makes CaImageViewer wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = CaImageViewer_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --------------------------------------------------------------------
function LoadFile_Callback(hObject, eventdata, handles)
% hObject    handle to LoadFile (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


global gui_CaImageViewer

%%% Get file information %%%

if ispc
    cd('Z:\People\Jake\Data')
elseif isunix 
    cd('/usr/local/lab/People/Jake/Data')
end

%%% Initialize/reset parameters and settings when loading new file
set(gui_CaImageViewer.figure.handles.MaxProjection_CheckBox, 'Value', 0);
set(gui_CaImageViewer.figure.handles.AveProjection_CheckBox, 'Value', 0);
set(gui_CaImageViewer.figure.handles.ImageSlider_Slider, 'Enable', 'on');
set(gui_CaImageViewer.figure.handles.Merge_ToggleButton, 'Value', 0)
if isempty(findobj('Type', 'figure', '-and', {'-regexp', 'Name', 'Multiple Sessions'}))
    gui_CaImageViewer.NewSpineAnalysis = 0;
else
    gui_CaImageViewer.NewSpineAnalysis = 1;
end
gui_CaImageViewer.SelectedStopFrame = [];
gui_CaImageViewer.IgnoreFrames = [];

[filename, pathname] = uigetfile('.tif');

if isnumeric(pathname) && isnumeric(filename)
    return
end

fname = [pathname, filename];

timecourse_image_number = [];

% fname = fname;
CaImage_File_info = imfinfo(fname);
timecourse_image_number = numel(CaImage_File_info);


gui_CaImageViewer.filename = filename;
gui_CaImageViewer.save_directory = pathname;
cd(pathname)
twochannels = get(gui_CaImageViewer.figure.handles.TwoChannels_CheckBox, 'Value');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%% Set Image Properties %%%

Green_Frame = 1;
Red_Frame = 1;

gui_CaImageViewer.GCaMP_Image = [];
gui_CaImageViewer.Red_Image = [];

h = waitbar(0, 'Loading Image ');
TifLink = Tiff(fname, 'r');

Green_loc = gui_CaImageViewer.GreenGraph_loc;
Red_loc = gui_CaImageViewer.RedGraph_loc;

if twochannels
    [Rfilename, Rpathname] = uigetfile('.tif', 'Select image file for the red channel');
    Rfname = [Rpathname, Rfilename];
    RTifLink = Tiff(Rfname, 'r');
    for i = 1:timecourse_image_number
        TifLink.setDirectory(i);
        gui_CaImageViewer.GCaMP_Image{1,Green_Frame} = TifLink.read();
        Green_Frame = Green_Frame+1;
        waitbar(Green_Frame/timecourse_image_number,h,['Loading Image ', num2str(Green_Frame)]);
        RTifLink.setDirectory(i);
        gui_CaImageViewer.Red_Image{1,Red_Frame} = RTifLink.read();
        Red_Frame = Red_Frame+1;
    end
    set(handles.RedGraph, 'Visible', 'on')
    set(handles.Channel2_StaticText, 'Visible', 'on')
    set(handles.RedUpperLUT_EditableText, 'Visible', 'on')
    set(handles.RedLowerLUT_EditableText, 'Visible', 'on')
    set(handles.RedGamma_EditableText, 'Visible', 'on')
    set(handles.RedGamma_StaticText, 'Visible', 'on')
    set(handles.GreenGraph, 'Units', 'normalized')
    set(handles.RedGraph, 'Units', 'normalized')
    figure(gui_CaImageViewer.figure.handles.figure1)
    axes(gui_CaImageViewer.figure.handles.GreenGraph);
    set(handles.GreenGraph, 'Position', [Green_loc(1), Red_loc(2), Red_loc(3), Red_loc(4)]);      %%% If an image using only 1 channel is already loaded, the "green" graph overlays the red, but the size of the original axes is maintained in the "red" graph.
    set(handles.RedGraph, 'Position', [Red_loc(1), Red_loc(2),  Red_loc(3), Red_loc(4)]);
else
    for i = 1:timecourse_image_number
        TifLink.setDirectory(i);
        gui_CaImageViewer.GCaMP_Image{1,Green_Frame} = TifLink.read();
        Green_Frame = Green_Frame+1;
        waitbar(Green_Frame/timecourse_image_number,h,['Loading Image ', num2str(Green_Frame)]);
    end
    set(handles.RedGraph, 'Visible', 'off')
    set(handles.Channel2_StaticText, 'Visible', 'off')
    set(handles.RedUpperLUT_EditableText, 'Visible', 'off')
    set(handles.RedLowerLUT_EditableText, 'Visible', 'off')
    set(handles.RedGamma_EditableText, 'Visible', 'off')
    set(handles.RedGamma_StaticText, 'Visible', 'off')
    gui_CaImageViewer.GraphPlacement = [Green_loc(1), Green_loc(2), Green_loc(3)+(Red_loc(1)-(Green_loc(1)+Green_loc(3))+Red_loc(3)), Green_loc(4)];
    set(handles.GreenGraph, 'Units', 'normalized')
    figure(gui_CaImageViewer.figure.handles.figure1)
    axes(gui_CaImageViewer.figure.handles.GreenGraph);
    intergraphdistance = Red_loc(1)-(Green_loc(1)+Green_loc(3));
    set(handles.GreenGraph, 'Position', [Green_loc(1), Green_loc(2), Green_loc(3)+Red_loc(3)+intergraphdistance, Green_loc(4)])
end

close(h)

channel1 = gui_CaImageViewer.GCaMP_Image;
channel2 = gui_CaImageViewer.Red_Image;

CommandSource = 'Loader';

[~, ~] = PlaceImages(channel1, channel2, CommandSource);

imageserieslength = size(gui_CaImageViewer.GCaMP_Image, 2);
gui_CaImageViewer.imageserieslength = imageserieslength;

set(handles.ImageSlider_Slider, 'Value', 1);
set(handles.ImageSlider_Slider, 'Min', 1);
set(handles.ImageSlider_Slider, 'Max', imageserieslength);
set(handles.ImageSlider_Slider, 'SliderStep', [(1/(imageserieslength-1)) (32/(imageserieslength-1))]);  %%% The Slider Step values indicate the minor and major transitions, which should be represented by the desired transition as the numerator and the length of the series as the denominator
set(handles.Frame_EditableText, 'String', 1);
set(handles.SmoothingFactor_EditableText, 'String', '1');

set(handles.SmoothingFactor_EditableText, 'String', 1);

set(gui_CaImageViewer.figure.handles.output, 'WindowButtonDownFcn', [])

gui_CaImageViewer.LoadedFile = 1;


% --- Executes on button press in MaxProjection_CheckBox.
function MaxProjection_CheckBox_Callback(hObject, eventdata, handles)
% hObject    handle to MaxProjection_CheckBox (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of MaxProjection_CheckBox

global gui_CaImageViewer
global zStack_Interface

val = get(handles.MaxProjection_CheckBox, 'Value');
set(handles.Frame_EditableText, 'String',1);

ImageNum = str2num(get(gui_CaImageViewer.figure.handles.Frame_EditableText, 'String'));
twochannels = get(gui_CaImageViewer.figure.handles.TwoChannels_CheckBox, 'Value');
filterwindow = str2num(get(gui_CaImageViewer.figure.handles.SmoothingFactor_EditableText, 'String'));
merged = get(gui_CaImageViewer.figure.handles.Merge_ToggleButton, 'Value');

if ishandle(zStack_Interface.figure)
    SliceFocus = regexp(zStack_Interface.CurrentSliceEdit.String, '[0-9]+_*', 'match');
    if zStack_Interface.LimittoSlice
        numslices = str2num(zStack_Interface.SlicesEdit.String);
        currentslice = str2double(SliceFocus{1});
        allmults = [currentslice:numslices:length(gui_CaImageViewer.GCaMP_Image)];       
        if isempty(find(allmults==ImageNum))
            [~, ind] = min(abs(allmults-ImageNum));
            ImageNum = allmults(ind);
        end
    else
        allmults = 1:length(gui_CaImageViewer.GCaMP_Image);
    end
    if length(SliceFocus)>1
        z_diff = str2double(SliceFocus{2})-str2double(SliceFocus{1});
    else
        z_diff = 0;
    end
end

if val
    set(handles.AveProjection_CheckBox, 'Value', 0);
    if ishandle(zStack_Interface.figure)
        im = gui_CaImageViewer.GCaMP_Image(allmults);
    else
        im = gui_CaImageViewer.GCaMP_Image;
    end
    im = cat(3, im{:});
    immax = max(im, [], 3); 
    
    if twochannels
        if ishandle(zStack_Interface.figure)
            overlim = (allmults+z_diff>length(gui_CaImageViewer.GCaMP_Image));
            if any(overlim)
                allmults = allmults(~overlim);
            end
            Rim = gui_CaImageViewer.GCaMP_Image(allmults+z_diff);
        else
            Rim = gui_CaImageViewer.Red_Image;
        end
        Rim = cat(3,Rim{:});
        Rimmax = max(Rim, [], 3);
    end
    
    
    if filterwindow == 1
    
        channel1 = immax;
        if twochannels && ~merged
            channel2 = Rimmax;
        elseif twochannels && merged
            channel1 = repmat(double(channel1)/max(max(double(channel1))),[1 1 3]);
            channel1(:,:,1) = zeros(size(channel1,1), size(channel1,2));
            channel1(:,:,3) = zeros(size(channel1,1), size(channel1,2));
            channel1(:,:,1) = double(Rimmax)/max(max(double(Rimmax)));
            channel2 = [];
        else
            channel2 = [];
        end

        CommandSource = 'Slider';

        %%%%%%%%%
        PlaceImages(channel1,channel2, CommandSource);
        %%%%%%%%%
    
    else
        smoothing_green = filter2(ones(filterwindow, filterwindow)/filterwindow^2, immax);
        channel1 = smoothing_green;
        if twochannels  && ~merged
            smoothing_red = filter2(ones(filterwindow, filterwindow)/filterwindow^2, Rimmax);
            channel2 = smoothing_red;
        elseif twochannels && merged
            channel1 = repmat(double(channel1)/max(max(double(channel1))),[1 1 3]);
            channel1(:,:,1) = zeros(size(channel1,1), size(channel1,2));
            channel1(:,:,3) = zeros(size(channel1,1), size(channel1,2));
            smoothing_red = filter2(ones(filterwindow, filterwindow)/filterwindow^2, Rimmax);
            channel1(:,:,1) = double(smoothing_red)/max(max(double(smoothing_red)));
            channel2 = [];
        else
            channel2 = [];
        end

        CommandSource = 'Slider';

        %%%%%%%%%
        PlaceImages(channel1,channel2, CommandSource);
        %%%%%%%%%
    end
else
    channel1 = gui_CaImageViewer.GCaMP_Image{ImageNum};
    
    if twochannels && ~merged
        if ishandle(zStack_Interface.figure)
            channel2 = gui_CaImageViewer.GCaMP_Image{ImageNum+z_diff};
        else
            channel2 = gui_CaImageViewer.Red_Image{ImageNum};
        end
    elseif twochannels && merged
            channel1 = repmat(double(channel1)/max(max(double(channel1))),[1 1 3]);
            channel1(:,:,1) = zeros(size(channel1,1), size(channel1,2));
            channel1(:,:,3) = zeros(size(channel1,1), size(channel1,2));
            channel1(:,:,1) = double(gui_CaImageViewer.Red_Image{ImageNum})/max(max(double(gui_CaImageViewer.Red_Image{ImageNum})));
            channel2 = [];
        else
            channel2 = [];
    end
        
    CaImageSlider(ImageNum);
end

% --- Executes on slider movement.
function ImageSlider_Slider_Callback(hObject, eventdata, handles)
% hObject    handle to ImageSlider_Slider (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider

global gui_CaImageViewer

% if isempty(eventdata)
    
    ImageNum = str2num(get(gui_CaImageViewer.figure.handles.Frame_EditableText, 'String'));
    CaImageSlider(ImageNum);

% else
%     if isempty(strfind(eventdata.Key, 'arrow'))
%        return
%     else
%         if strcmpi(eventdata.Key, 'rightarrow')
%             ImageNum = str2num(get(gui_CaImageViewer.figure.handles.Frame_EditableText, 'String'))+1;
%             CaImageSlider(ImageNum);
%         elseif strcmpi(eventdata.Key, 'leftarrow')
%             ImageNum = str2num(get(gui_CaImageViewer.figure.handles.Frame_EditableText, 'String'))-1;
%                 if ImageNum < 1
%                     ImageNum = 1;
%                 end
%             CaImageSlider(ImageNum);
%         end
%     end
% end


% --- Executes during object creation, after setting all properties.
function ImageSlider_Slider_CreateFcn(hObject, eventdata, handles)
% hObject    handle to ImageSlider_Slider (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end



% figure_children = get(gui_CaImageViewer.figure.handles.output, 'Children');
% figure_axes = findobj(figure_children, 'Type', 'axes');
% set(findobj(figure_children, 'Type', 'axes'), 'ButtonDownFcn', @Ca_DrawROI);
% red_axes_children = get(figure_axes(1), 'Children');
% green_axes_children = get(figure_axes(2), 'Children');

% set(findobj(green_axes_children, 'Type', 'Image'), 'ButtonDownFcn', @Ca_DrawROI);
% set(findobj(red_axes_children, 'Type', 'Image'), 'ButtonDownFcn', @Ca_DrawROI);


function Frame_EditableText_Callback(hObject, eventdata, handles)
% hObject    handle to Frame_EditableText (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of Frame_EditableText as text
%        str2double(get(hObject,'String')) returns contents of Frame_EditableText as a double


% --- Executes during object creation, after setting all properties.
function Frame_EditableText_CreateFcn(hObject, eventdata, handles)
% hObject    handle to Frame_EditableText (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

global gui_CaImageViewer
    


% --- Executes on button press in CalcROIs_PushButton.
function CalcROIs_PushButton_Callback(hObject, eventdata, handles)
% hObject    handle to CalcROIs_PushButton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


CaCalculateROIs



function UpperLUT_EditableText_Callback(hObject, eventdata, handles)
% hObject    handle to UpperLUT_EditableText (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of UpperLUT_EditableText as text
%        str2double(get(hObject,'String')) returns contents of UpperLUT_EditableText as a double


% --- Executes during object creation, after setting all properties.
function UpperLUT_EditableText_CreateFcn(hObject, eventdata, handles)
% hObject    handle to UpperLUT_EditableText (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function LowerLUT_EditableText_Callback(hObject, eventdata, handles)
% hObject    handle to LowerLUT_EditableText (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of LowerLUT_EditableText as text
%        str2double(get(hObject,'String')) returns contents of LowerLUT_EditableText as a double


% --- Executes during object creation, after setting all properties.
function LowerLUT_EditableText_CreateFcn(hObject, eventdata, handles)
% hObject    handle to LowerLUT_EditableText (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function SmoothingFactor_EditableText_Callback(hObject, eventdata, handles)
% hObject    handle to SmoothingFactor_EditableText (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of SmoothingFactor_EditableText as text
%        str2double(get(hObject,'String')) returns contents of SmoothingFactor_EditableText as a double


% --- Executes during object creation, after setting all properties.
function SmoothingFactor_EditableText_CreateFcn(hObject, eventdata, handles)
% hObject    handle to SmoothingFactor_EditableText (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in ViewMovie_Checkbox.
function ViewMovie_Checkbox_Callback(hObject, eventdata, handles)
% hObject    handle to ViewMovie_Checkbox (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of ViewMovie_Checkbox
global gui_CaImageViewer


% --- Executes on button press in BackgroundROI_ToggleButton.
function BackgroundROI_ToggleButton_Callback(hObject, eventdata, handles)
% hObject    handle to BackgroundROI_ToggleButton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of BackgroundROI_ToggleButton

global gui_CaImageViewer

% set(gui_CaImageViewer.figure.handles.ZoomIn_ToggleTool, 'state', 'off')
% set(gui_CaImageViewer.figure.handles.ZoomOut_ToggleTool, 'state', 'off')
% set(gui_CaImageViewer.figure.handles.Pan_ToggleTool, 'state', 'off')

BackgroundROI = get(gui_CaImageViewer.figure.handles.BackgroundROI_ToggleButton, 'Value');
SpineROI = get(gui_CaImageViewer.figure.handles.SpineROI_ToggleButton, 'Value');
NearbySpineROI = get(gui_CaImageViewer.figure.handles.DrawOther_ToggleButton, 'Value');
Dendrite_PolyLines = get(gui_CaImageViewer.figure.handles.DendritePolyLines_ToggleButton, 'Value');
Router = 'Background';

if BackgroundROI == 1
    set(handles.SpineROI_ToggleButton, 'Value', 0);
    set(handles.DrawOther_ToggleButton, 'Value', 0);
    set(handles.DendritePolyLines_ToggleButton, 'Value', 0);
    set(gui_CaImageViewer.figure.handles.output, 'WindowButtonDownFcn', {@DrawROI, 0, Router});
end

if BackgroundROI == 0 && SpineROI == 0 && NearbySpineROI == 0 && Dendrite_PolyLines == 0
    set(gui_CaImageViewer.figure.handles.output, 'WindowButtonDownFcn', []);
end


% --- Executes on button press in SpineROI_ToggleButton.
function SpineROI_ToggleButton_Callback(hObject, eventdata, handles)
% hObject    handle to SpineROI_ToggleButton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of SpineROI_ToggleButton

global gui_CaImageViewer

BackgroundROI = get(gui_CaImageViewer.figure.handles.BackgroundROI_ToggleButton, 'Value');
SpineROI = get(gui_CaImageViewer.figure.handles.SpineROI_ToggleButton, 'Value');
NearbySpineROI = get(gui_CaImageViewer.figure.handles.DrawOther_ToggleButton, 'Value');
Dendrite_PolyLines = get(gui_CaImageViewer.figure.handles.DendritePolyLines_ToggleButton, 'Value');
ROInum = gui_CaImageViewer.Spine_Number + 1;

ROIs = findobj(gui_CaImageViewer.figure.handles.GreenGraph, 'Type', 'images.roi.ellipse', '-and', '-not', {'-regexp', 'Tag', 'Dendrite'});

for i = 1:length(ROIs)
    ROIs(i).InteractionsAllowed = 'none';
end

Router = 'Spine';

if SpineROI == 1
    set(handles.BackgroundROI_ToggleButton, 'Value', 0);
    set(handles.DrawOther_ToggleButton, 'Value', 0);
    set(handles.DendritePolyLines_ToggleButton, 'Value', 0);
    set(gui_CaImageViewer.figure.handles.output, 'WindowButtonDownFcn', {@DrawROI, ROInum, Router})
    set(gui_CaImageViewer.figure.handles.InsertSpine_ToggleButton, 'Enable', 'on')
end

if BackgroundROI == 0 && SpineROI == 0 && NearbySpineROI == 0 && Dendrite_PolyLines == 0
    set(gui_CaImageViewer.figure.handles.output, 'WindowButtonDownFcn', []);
end

% --- Executes on button press in ClearROIS_PushButton.
function ClearROIS_PushButton_Callback(hObject, eventdata, handles)
% hObject    handle to ClearROIS_PushButton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


ClearROIs('Query')


% --- Executes on button press in DrawOther_ToggleButton.
function DrawOther_ToggleButton_Callback(hObject, eventdata, handles)
% hObject    handle to DrawOther_ToggleButton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of DrawOther_ToggleButton

global gui_CaImageViewer;

BackgroundROI = get(gui_CaImageViewer.figure.handles.BackgroundROI_ToggleButton, 'Value');
SpineROI = get(gui_CaImageViewer.figure.handles.SpineROI_ToggleButton, 'Value');
DrawOtherROI = get(gui_CaImageViewer.figure.handles.DrawOther_ToggleButton, 'Value');
Dendrite_PolyLines = get(gui_CaImageViewer.figure.handles.DendritePolyLines_ToggleButton, 'Value');
ROInum = length(gui_CaImageViewer.ROIother);
Router = 'Other';

twochannels = gui_CaImageViewer.figure.handles.TwoChannels_CheckBox.Value;
Merge = gui_CaImageViewer.figure.handles.Merge_ToggleButton.Value;

if DrawOtherROI == 1
    set(handles.BackgroundROI_ToggleButton, 'Value', 0);
    set(handles.SpineROI_ToggleButton, 'Value', 0);
    set(handles.DendritePolyLines_ToggleButton, 'Value', 0);
    set(gui_CaImageViewer.figure.handles.output, 'WindowButtonDownFcn', {@DrawROI, ROInum, Router})
end

if BackgroundROI == 0 && SpineROI == 0 && DrawOtherROI == 0 && Dendrite_PolyLines == 0
    set(gui_CaImageViewer.figure.handles.output, 'WindowButtonDownFcn', []);
end

% --- Executes on button press in DendritePolyLines_ToggleButton.
function DendritePolyLines_ToggleButton_Callback(hObject, eventdata, handles)
% hObject    handle to DendritePolyLines_ToggleButton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of DendritePolyLines_ToggleButton

global gui_CaImageViewer;


BackgroundROI = get(gui_CaImageViewer.figure.handles.BackgroundROI_ToggleButton, 'Value');
SpineROI = get(gui_CaImageViewer.figure.handles.SpineROI_ToggleButton, 'Value');
NearbySpineROI = get(gui_CaImageViewer.figure.handles.DrawOther_ToggleButton, 'Value');
Dendrite_PolyLines = get(gui_CaImageViewer.figure.handles.DendritePolyLines_ToggleButton, 'Value');
CurrentDendNum = gui_CaImageViewer.Dendrite_Number+1;

if Dendrite_PolyLines == 1
    set(handles.BackgroundROI_ToggleButton, 'Value', 0);
    set(handles.SpineROI_ToggleButton, 'Value', 0);
    set(handles.DrawOther_ToggleButton, 'Value', 0);
        DendriteNum = inputdlg({'Dendrite number:'}, 'Input', 1, {num2str(CurrentDendNum)});
        if isempty(DendriteNum)
            return
        end
    DendriteNum = str2num(DendriteNum{1});
    set(gui_CaImageViewer.figure.handles.output, 'WindowButtonDownFcn', {@DrawPolyLines, DendriteNum});
end

if BackgroundROI == 0 && SpineROI == 0 && NearbySpineROI == 0 && Dendrite_PolyLines == 0
    set(gui_CaImageViewer.figure.handles.output, 'WindowButtonDownFcn', []);
end



function RedUpperLUT_EditableText_Callback(hObject, eventdata, handles)
% hObject    handle to RedUpperLUT_EditableText (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of RedUpperLUT_EditableText as text
%        str2double(get(hObject,'String')) returns contents of RedUpperLUT_EditableText as a double


% --- Executes during object creation, after setting all properties.
function RedUpperLUT_EditableText_CreateFcn(hObject, eventdata, handles)
% hObject    handle to RedUpperLUT_EditableText (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function RedLowerLUT_EditableText_Callback(hObject, eventdata, handles)
% hObject    handle to RedLowerLUT_EditableText (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of RedLowerLUT_EditableText as text
%        str2double(get(hObject,'String')) returns contents of RedLowerLUT_EditableText as a double


% --- Executes during object creation, after setting all properties.
function RedLowerLUT_EditableText_CreateFcn(hObject, eventdata, handles)
% hObject    handle to RedLowerLUT_EditableText (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function Zoom_EditableText_Callback(hObject, eventdata, handles)
% hObject    handle to Zoom_EditableText (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of Zoom_EditableText as text
%        str2double(get(hObject,'String')) returns contents of Zoom_EditableText as a double


% --- Executes during object creation, after setting all properties.
function Zoom_EditableText_CreateFcn(hObject, eventdata, handles)
% hObject    handle to Zoom_EditableText (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --------------------------------------------------------------------
function CodeEdit_Callback(hObject, eventdata, handles)
% hObject    handle to CodeEdit (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

edit CaImageViewer



function GreenGamma_EditableText_Callback(hObject, eventdata, handles)
% hObject    handle to GreenGamma_EditableText (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of GreenGamma_EditableText as text
%        str2double(get(hObject,'String')) returns contents of GreenGamma_EditableText as a double


% --- Executes during object creation, after setting all properties.
function GreenGamma_EditableText_CreateFcn(hObject, eventdata, handles)
% hObject    handle to GreenGamma_EditableText (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function RedGamma_EditableText_Callback(hObject, eventdata, handles)
% hObject    handle to RedGamma_EditableText (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of RedGamma_EditableText as text
%        str2double(get(hObject,'String')) returns contents of RedGamma_EditableText as a double


% --- Executes during object creation, after setting all properties.
function RedGamma_EditableText_CreateFcn(hObject, eventdata, handles)
% hObject    handle to RedGamma_EditableText (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in TwoChannels_CheckBox.
function TwoChannels_CheckBox_Callback(hObject, eventdata, handles)
% hObject    handle to TwoChannels_CheckBox (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of TwoChannels_CheckBox

twochannels = get(handles.TwoChannels_CheckBox, 'Value');

if twochannels
    set(handles.Merge_ToggleButton, 'Enable', 'on')
else
    set(handles.Merge_ToggleButton, 'Enable', 'off')
end

% --- Executes on button press in RecoverROIs_PushButton.
function RecoverROIs_PushButton_Callback(hObject, eventdata, handles)
% hObject    handle to RecoverROIs_PushButton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

%%% Set general running variables %%%%%

global gui_CaImageViewer
glovar = gui_CaImageViewer;
axes1 = glovar.figure.handles.GreenGraph;
axes2 = glovar.figure.handles.RedGraph;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% File Specifications

try
    file = gui_CaImageViewer.filename;
    file = file(1:end-4);
    experiment = regexp(gui_CaImageViewer.filename, '[A-Z]{2}\d+[_]\d+', 'match');
    experiment = experiment{1};
    animal = experiment(1:5);
catch
    experiment = regexp(gui_CaImageViewer.filename, '[A-Z]{2,3}\w+', 'match');
    if ~isempty(experiment)
        experiment = experiment{1};
        animal = experiment(1:5);
    else
        filenameparts = regexp(gui_CaImageViewer.filename, '[0]{2,4}[1-9]{1,3}_[0]{2,4}[1-9]{1,3}', 'split');
        experiment = filenameparts{1};
    end
end

twochannels = get(glovar.figure.handles.TwoChannels_CheckBox, 'Value');

% if ispc
    save_directory = gui_CaImageViewer.save_directory;
% else
%     nameparts = regexp(gui_CaImageViewer.save_directory, filesep, 'split');
%     linuxstarter = '/usr/local/lab/';
%     save_directory = [linuxstarter, nameparts{2}, filesep, nameparts{3}, filesep, nameparts{4}, filesep, nameparts{5}, filesep, nameparts{6}, filesep, nameparts{7},filesep];
% end

try
    cd(save_directory)
    folder = dir(save_directory);
catch
    disp('Could not connect to saved directory... will need to select manually');
    folder = [];
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% Find all files that hold ROI positions
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Scrsz = get(0, 'Screensize');
User = get(gui_CaImageViewer.figure.handles.figure1, 'UserData');

count = 1;
roifile = [];
found = 0;

ForceManual = 1;

if gui_CaImageViewer.NewSpineAnalysis
    for i = 1:length(folder)
        match = regexp(folder(i).name, 'NewSpineAnalysisROIs');
        if ~isempty(match)
            roifile{count} = folder(i).name;
            count = count+1;
            found = 1;
        end
    end
else
    for i = 1:length(folder)
        match = regexp(folder(i).name, [experiment, '_SavedROIs_DrawnBy', User]);
        if ~isempty(match)
            roifile{count} = folder(i).name;
            count = count+1;
            found = 1;
        end
    end
end

if ~found || ForceManual
    boxwidth = 250;
    d = dialog('Position', [(Scrsz(3)/2)-125 Scrsz(4)/2-75 boxwidth 150], 'Name', 'No user-specific ROI file');
    txt = uicontrol('Parent', d, 'Style', 'text', 'Position', [10 100 230 30], 'String', 'No user-specific ROI file... manually select or automatically find one?');
    buttonwidth = 50;
    uicontrol('Parent', d, 'Style', 'pushbutton', 'Position', [boxwidth/2-buttonwidth-10 30 buttonwidth 25], 'String', 'Manual', 'Callback', @DlgChoice)
    uicontrol('Parent', d, 'Style', 'pushbutton', 'Position', [boxwidth/2+10 30 buttonwidth 25], 'String', 'Auto', 'Callback', @DlgChoice)
    uiwait(d)
    choice = get(d,'UserData');
    delete(d);
    if strcmpi(choice, 'Manual')
        [roifilename, roipath] = uigetfile();
        if isnumeric(roifilename) && isnumeric(roipath)
            return
        end
        cd(roipath)
    elseif strcmpi(choice, 'Auto')
        count = 1;
        roifile = [];
        if gui_CaImageViewer.NewSpineAnalysis
            for i = 1:length(folder)
                match = regexp(folder(i).name, 'NewSpineAnalysisROIs', 'once');
                if ~isempty(match)
                    roifile{count} = folder(i).name;
                    count = count+1;
                end
            end
        else
            for i = 1:length(folder)
                match = regexp(folder(i).name, [experiment, '_SavedROIs'], 'once');
                if ~isempty(match)
                    roifile{count} = folder(i).name;
                    count = count+1;
                end
            end
        end
        if length(roifile)>1
            for i = 1:length(roifile)
                temp = regexp(roifile{i}, 'DrawnBy', 'split');
                if length(temp)>1           
                    useroption{i} = temp{2}(1:end-4);
                else
                    useroption{i} = 'undefined';    %%% If the file doesn't contain the "DrawnBy" tag, then it will only return 1 answer, and therefore was made prior to qualifying the file according to username
                end
            end
            d = dialog('Position', [(Scrsz(3)/2)-125 Scrsz(4)/2-75 250 150], 'Name', 'Found multiple ROI files...');
            txt = uicontrol('Parent', d, 'Style', 'text', 'Position', [10 100 230 30], 'String', 'Load ROIs drawn by whom?');
            for j = 1:length(roifile)
                uicontrol('Parent', d, 'Style', 'pushbutton', 'Position', [30+((j-1)*55) 30 50 25], 'String', useroption{j}, 'Callback', @DlgChoice)
            end
            uiwait(d)
            choice = get(d, 'UserData');
            delete(d);
            roifilename = roifile{find(~cell2mat(cellfun(@isempty, (cellfun(@(x) strfind(x, choice), roifile, 'uni', false)), 'uni', false)))};     %%% To avoid issues with file naming, use the original file names that were found, finding the one that contains the name chosen
        else
            roifilename = roifile{1}(1:end-4);
        end
    end
else
    roifilename = roifile{1}(1:end-4);
end

load(roifilename)
savedFile = roifilename;
disp('Successfully pulled ROIs from saved ROI file')
cd(gui_CaImageViewer.save_directory)

try
    eval(['savedFile =', savedFile]);
catch
    if ~isempty(savedFile)
        temp = who(['*',savedFile(1:5), '*']);
        savedFile = temp{1};
        disp('File name discrepancy; using closest available')
        eval(['savedFile =', savedFile]);
    end
end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%% Draw loaded ROIs %%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if isstruct(savedFile.ROIPosition{1})
    drawtype = 'new';
    for i = 1:length(savedFile.ROIPosition)
        ROIs(i).Center = savedFile.ROIPosition{i}.Center;
        ROIs(i).SemiAxes = savedFile.ROIPosition{i}.SemiAxes;
        ROIs(i).RotationAngle = savedFile.ROIPosition{i}.RotationAngle;
        ROIs(i).AspectRatio = savedFile.ROIPosition{i}.AspectRatio;
    end
    if isfield(savedFile, 'OtherROIs')
        OtherROIsExist = 1;
        for i = 1:length(savedFile.OtherROIs)
            OtherROIs(i).Position = savedFile.OtherROIsPosition{i}.Position;
        end
    else
        OtherROIsExist = 0;
    end
else
    drawtype = 'old';
    oldROIs = savedFile.ROIPosition;
    for i = 1:length(oldROIs)
        ROIcenter = [oldROIs{i}(1)+oldROIs{i}(3)/2, oldROIs{i}(2)+oldROIs{i}(4)/2];
        ROISemiAxes = [oldROIs{i}(3)/2, oldROIs{i}(4)/2];
        ROIs(i).Center = ROIcenter;
        ROIs(i).SemiAxes = ROISemiAxes;
        ROIs(i).RotationAngle = 0;
        ROIs(i).AspectRatio = oldROIs{i}(3)/oldROIs{i}(4);
    end
    if isfield(savedFile, 'OtherROIs')
        OtherROIsExist = 1;
        for i = 1:length(savedFile.OtherROIs)
            OtherROIs(i).Position = savedFile.OtherROIsPosition{i}.Position;
        end
    else
        OtherROIsExist = 0;
    end
end

glovar.Spine_Number = length(ROIs)-1;

dlgwdth = 250;
d = dialog('Position', [(Scrsz(3)/2)-125 Scrsz(4)/2-75 dlgwdth 150], 'Name', 'Surround ROI option');
uicontrol('Parent', d, 'Style', 'text', 'Position', [10 100 230 30], 'String', 'Draw surround background ROIs?');
uicontrol('Parent', d, 'Style', 'pushbutton', 'Position', [dlgwdth/3-75 30 100 25], 'String', 'Recover previous', 'Callback', @DlgChoice)
uicontrol('Parent', d, 'Style', 'pushbutton', 'Position', [dlgwdth/3+30 30 50 25], 'String', 'No', 'Callback', @DlgChoice)
uicontrol('Parent', d, 'Style', 'pushbutton', 'Position', [dlgwdth/3+85 30 75 25], 'String', 'Add to all', 'Callback', @DlgChoice)
uiwait(d)
usesurroundBGchoice = get(d, 'UserData');
delete(d);
nonedrawn = 0;

axes(axes1);
for a = 1:length(ROIs)
    ROInum = a-1;
    glovar.ROI(a) = drawellipse('Center', ROIs(a).Center, 'SemiAxes', ROIs(a).SemiAxes, 'RotationAngle', ROIs(a).RotationAngle,...
        'AspectRatio', ROIs(a).AspectRatio, 'Tag', ['ROI', num2str(ROInum)], 'Color', [0.2 0.4 0.9],...
        'HandleVisibility', 'on', 'Label', '', 'Linewidth', 1, 'FaceAlpha', 0, 'InteractionsAllowed', 'none');
    roiget = get(glovar.ROI(a));
    mtlbver = ver;
    if contains(mtlbver(1).Release, '2021')
        c = roiget.ContextMenu;
    else
        c = roiget.UIContextMenu;
    end
    uimenu(c, 'Label', 'Add Surround Background', 'Callback', @ModifyROI);
    uimenu(c, 'Label', 'Remove Surround Background', 'Callback', @ModifyROI);
    uimenu(c, 'Label', 'Set as eliminated', 'Callback', @CategorizeSpines);
    uimenu(c, 'Label', 'Set as active', 'Callback', @CategorizeSpines);
    set(glovar.figure.handles.ShowLabels_ToggleButton, 'Value', 1)
    glovar.ROIlistener{ROInum+1} = listener(findobj(glovar.ROI(a)), 'DeletingROI', @DeleteROI);
    addlistener(findobj(glovar.ROI(a)), 'ROIClicked', @DeclareROI);
    switch usesurroundBGchoice
        case 'Add to all'
            if a == 1   %%% The first ROI (the general background ROI) doesn't need an additional background
                glovar.BackgroundROI(a) = NaN;
                continue
            end
            surroundoffset = glovar.SurroundBackgroundBuffer;
            glovar.BackgroundROI(ROInum+1) = rectangle('Position', [ROIs{a}(1)-surroundoffset/2, ROIs{a}(2)-surroundoffset/2, ROIs{a}(3)+surroundoffset, ROIs{a}(4)+surroundoffset], 'EdgeColor', 'w', 'Curvature', [1 1], 'Tag', ['BackgroundROI', num2str(ROInum)], 'Linewidth', 0.75);
            glovar.UsingSurroundBackground = 1;
        case 'Recover previous'
            if isfield(savedFile, 'BackgroundROIPosition')
                if ~isempty(savedFile.BackgroundROIPosition{a})
                    glovar.BackgroundROI(ROInum+1) = rectangle('Position', savedFile.BackgroundROIPosition{a}, 'EdgeColor', 'w', 'Curvature', [1 1], 'Tag', ['BackgroundROI', num2str(ROInum)], 'Linewidth', 0.75);
                else
                    glovar.BackgroundROI(ROInum+1) = NaN;
                end
            else
                usesurroundBGchoice = 'No';
                nonedrawn = 1;
                glovar.UsingSurroundBackground = 0;
                glovar.BackgroundROI(ROInum+1) = NaN;
            end
        case 'No'
            glovar.UsingSurroundBackground = 0;
            glovar.BackgroundROI(ROInum+1) = NaN;
    end
    if twochannels == 1
        axes(axes2);
        glovar.ROIred(a) = drawellipse('Center', ROIs(a).Center, 'SemiAxes', ROIs(a).SemiAxes, 'RotationAngle', ROIs(a).RotationAngle,...
        'AspectRatio', ROIs(a).AspectRatio, 'Tag', ['ROIred', num2str(ROInum)], 'Color','c',...
        'HandleVisibility', 'on', 'UIContextMenu', c, 'Label', '', 'Linewidth', 1, 'FaceAlpha', 0, 'InteractionsAllowed', 'none');
        roiget = get(glovar.ROIred(a));
        c = roiget.UIContextMenu;
        uimenu(c, 'Label', 'Add Surround Background', 'Callback', @ModifyROI);
        uimenu(c, 'Label', 'Remove Surround Background', 'Callback', @ModifyROI);
        uimenu(c, 'Label', 'Set as eliminated', 'Callback', @CategorizeSpines);
        uimenu(c, 'Label', 'Set as active', 'Callback', @CategorizeSpines);
        set(glovar.figure.handles.ShowLabels_ToggleButton, 'Value', 1)        
        axes(axes1);
    else
    end
end

if nonedrawn
    msgbox('Surround ROIs were not drawn for this file!');
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% New spine analysis section
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if glovar.NewSpineAnalysis
    drawer = get(gui_CaImageViewer.figure.handles.figure1, 'UserData');
    if ~isempty(drawer)
        userspecificpart = [drawer,'_'];
    else
        userspecificpart = [];
    end
    terminus = regexp(save_directory, animal, 'end');
    targ_folder = save_directory(1:terminus);
    currentfield = glovar.NewSpineAnalysisInfo.CurrentImagingField;
    if isempty(currentfield)
        cf = inputdlg('No field number found; Enter field number:', '1', 1);
        currentfield = str2num(cf{1});
        glovar.NewSpineAnalysisInfo.CurrentImagingField = currentfield; 
    end
    try
        load([targ_folder, filesep,userspecificpart,'Imaging Field ', num2str(currentfield), ' Spine Registry'])
    catch
        warning('No Spine Registry file found... make sure to make a new one or check if it was saved somewhere else!')
        [fname, pname] = uigetfile();
        load([pname, fname])
    end
    instanceofappearance = find(logical(strcmpi(SpineRegistry.DatesAcquired, gui_CaImageViewer.NewSpineAnalysisInfo.CurrentDate)));
    glovar.NewSpineAnalysisInfo.SpineList = ones(1,length(ROIs)-1); %%% Don't forget the first ROI is always the background ROI!
%     if size(SpineRegistry.Data,2)>=find(instanceofappearance) %% && find(instanceofappearance)~=1 %%% ZL commentm, it is possible need to set another category of spines specifying the "true new spines"
        if ~isempty(SpineRegistry.Data) && size(SpineRegistry.Data,2)>=instanceofappearance
            r = find(SpineRegistry.Data(:,instanceofappearance)==0);
            for i = 1:length(r)
                set(findobj(glovar.figure.handles.GreenGraph, 'Type', 'rectangle', 'Tag', ['ROI', num2str(r(i))]), 'FaceColor', [1 0 0])
            end
            glovar.NewSpineAnalysisInfo.SpineList(r) = 0;
        end
end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%% Handle dendritic ROIs %%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

DendNum = savedFile.NumberofDendrites; glovar.Dendrite_Number = DendNum;
coordinates = savedFile.PolyLinePosition;
PPnum = cumsum(savedFile.DendritePolyPointNumber);
glovar.SpineDendriteGrouping = savedFile.SpineDendriteGrouping;

radius = 3;
x = [];
x_red = [];
y = [];
y_red = [];

if isfield(glovar, 'PolyROI') && ~isempty(coordinates)
    PPsperDend = savedFile.DendritePolyPointNumber;
    if PPsperDend == 0
        warning('Dendrite ROIs could not be returned and must be redrawn')
        glovar.Dendrite_Number = 0;
        gui_CaImageViewer = glovar;
        return
    else
        glovar.DendritePolyPointNumber = PPsperDend;
        Dendrite_ROIs = length(savedFile.PolyROI);
    end
    if ~isempty(coordinates{1})
    axes(axes1);
    currDend = 1;
    polycount = 1;
        for i = 1:length(coordinates)
            switch drawtype
                case 'old'
                    glovar.PolyLinePos{i} = [coordinates{i}(1), coordinates{i}(2), radius, radius];
                    glovar.PolyROI{i} = rectangle('Position', glovar.PolyLinePos{i}, 'EdgeColor', 'g', 'Tag', ['Dendrite ', num2str(currDend), ' PolyROI ', num2str(polycount)],...
                        'Curvature', [1 1], 'ButtonDownFcn', 'Drag_Poly');
                    x = [x,coordinates{i}(1)+radius];
                    y = [y,coordinates{i}(2)+radius];
                case 'new'
                    glovar.PolyLinePos{i} = savedFile.PolyROI{i}.Center;
                    glovar.PolyROI{i} = drawellipse('Center', savedFile.PolyROI{i}.Center,'RotationAngle', savedFile.PolyROI{i}.RotationAngle, 'SemiAxes', savedFile.PolyROI{i}.SemiAxes,...
                        'AspectRatio', savedFile.PolyROI{i}.AspectRatio, 'Tag', ['Dendrite ', num2str(currDend), ' PolyROI ', num2str(polycount)], 'FaceAlpha', 0, 'Color', 'g', 'DrawingArea',...
                        'unlimited', 'HandleVisibility', 'on','InteractionsAllowed', 'none', 'Linewidth', 1);
                    x = [x,savedFile.PolyROI{i}.Center(1)];
                    y = [y,savedFile.PolyROI{i}.Center(2)];
            end
            if i < sum(PPsperDend(1:currDend))
                polycount = polycount+1;
            else
                currDend = currDend+1;
                polycount = 1;
            end
        end
        if DendNum == 1
%                 for i = 1:2:length(glovar.PolyLinePos)
                hold on;
                plot(x,y, 'color', 'cyan', 'Tag', 'PolyLine 1');
%                 end
        else
            counter = 1;
            for i = 1:DendNum
                hold on;
                plot(x(counter:(counter+PPsperDend(i)-1)),y(counter:(counter+PPsperDend(i)-1)), 'color', 'cyan', 'Tag', ['PolyLine ', num2str(i)]);
                counter = sum(PPsperDend(1:i))+1;
            end
        end
    end
end    

if OtherROIsExist
    if twochannels
        axes(axes2)
        for i = 1:length(OtherROIs)
            glovar.ROIother(i) = drawfreehand('Position', OtherROIs(i).Position, 'Tag', ['ROIother', num2str(i)], 'FaceAlpha', 0, 'Color', 'm', 'HandleVisibility', 'on', 'Label', num2str(i), 'InteractionsAllowed', 'none', 'Label', '');
        end
        axes(axes1)
    else
    end
else
end

 %%% Overwrite the previous existing global workspace with the newly imprinted one
 
set(glovar.figure.handles.EditSpines_ToggleButton, 'Value', 0)
 
gui_CaImageViewer = glovar;

function BaselineFrames_EditableText_Callback(hObject, eventdata, handles)
% hObject    handle to BaselineFrames_EditableText (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of BaselineFrames_EditableText as text
%        str2double(get(hObject,'String')) returns contents of BaselineFrames_EditableText as a double


% --- Executes during object creation, after setting all properties.
function BaselineFrames_EditableText_CreateFcn(hObject, eventdata, handles)
% hObject    handle to BaselineFrames_EditableText (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --------------------------------------------------------------------
function File_Callback(hObject, eventdata, handles)
% hObject    handle to File (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

    

% --- Executes on button press in SaveROIs_PushButton.
function SaveROIs_PushButton_Callback(hObject, eventdata, handles)
% hObject    handle to SaveROIs_PushButton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and  data (see GUIDATA)

global gui_CaImageViewer

drawer = get(gui_CaImageViewer.figure.handles.figure1, 'UserData');

a.SpineROIs = gui_CaImageViewer.ROI;
a.SpineROItext = gui_CaImageViewer.ROItext;
a.PolyROI = gui_CaImageViewer.PolyROI;
a.BackgroundROIs = gui_CaImageViewer.BackgroundROI;

try
    a.PolyLines = gui_CaImageViewer.PolyLine;
catch
    a.PolyLines = [];
end

a.PolyLinePosition = gui_CaImageViewer.PolyLinePos;
a.PolyROIPos = gui_CaImageViewer.PolyLinePos;
a.PolyLineVertices = gui_CaImageViewer.PolyLineVertices;
a.NumberofSpines = gui_CaImageViewer.Spine_Number;
a.OtherROIs = gui_CaImageViewer.ROIother;
a.OtherROINumber = length(gui_CaImageViewer.ROIother);

if a.SpineROIs(1) == 0
    msgbox('Cannot save ROIs without drawing background!');
    return
end

roiType = get(gui_CaImageViewer.ROI(1), 'Type');
if ~isempty(gui_CaImageViewer.ROIother)
    OtherROIsExist = 1;
    for i = 1:length(gui_CaImageViewer.ROIother)
        a.OtherROIsPosition{i} = get(a.OtherROIs(i));
    end
else
    OtherROIsExist = 0;
end

switch roiType  %%% ROI drawing method changed for release 2018 to use elliptical objects, native to MatLab software
    case 'rectangle'
        for i = 1:length(a.SpineROIs)
            a.ROIPosition{i} = get(a.SpineROIs(i), 'Position');
        end
    case 'images.roi.ellipse'
        for i = 1:length(a.SpineROIs)
            a.ROIPosition{i} = get(a.SpineROIs(i));
        end
end

for i = 1:length(a.BackgroundROIs)
    if ~isnan(a.BackgroundROIs(i)) && a.BackgroundROIs(i)
        a.BackgroundROIPosition{i} = get(a.BackgroundROIs(i), 'Position');
    else
        a.BackgroundROIPosition{i} = [];
    end
end

a.NumberofDendrites = gui_CaImageViewer.Dendrite_Number;
a.DendritePolyPointNumber = gui_CaImageViewer.DendritePolyPointNumber;

DendNum = gui_CaImageViewer.Dendrite_Number;

if DendNum > 1
    prompt = cell(1,DendNum);
    for i = 1:length(prompt)
        prompt{i} = ['Spines on dendrite ', num2str(i)];
    end
    name = 'Spine Grouping';
    numlines = 1;
    defaultanswer = cell(1,DendNum);
    for i = 1:length(defaultanswer)
        if ~isempty(gui_CaImageViewer.SpineDendriteGrouping)
            try
                first = min(gui_CaImageViewer.SpineDendriteGrouping{i});
                last = max(gui_CaImageViewer.SpineDendriteGrouping{i});
                defaultanswer{i} = sprintf('%d:%d', first, last);
            catch
                defaultanswer{i} = '';
            end
        else
            defaultanswer{i} = '';
        end
    end
    s_d_grouping = inputdlg(prompt, name, numlines, defaultanswer);
    for i = 1:DendNum
        DendSpines{i} = str2num(s_d_grouping{i});
    end
else 
    DendSpines{1} = 1:length(a.SpineROIs)-1;
end

a.SpineDendriteGrouping = DendSpines;

gui_CaImageViewer.SpineDendriteGrouping = DendSpines;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% New Spine Analysis Section
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if gui_CaImageViewer.NewSpineAnalysis
    animal = regexp(gui_CaImageViewer.filename, '[A-Z]{2,3}[0-9]*', 'match');
    animal = animal{1};
    date = regexp(gui_CaImageViewer.save_directory, '[0-9]{5,7}', 'match');
    if isempty(date)
        date = inputdlg('No date found; enter here:', 'Exp. Date', 1, {'YYMMDD'});
    end
    experiment = [animal, '_', date{1}];
    fname = [experiment, '_NewSpineAnalysisROIs', '_DrawnBy', drawer];
    
        %%%%% Move to parent folder
        fullpath = gui_CaImageViewer.save_directory;
        allseps = strfind(fullpath, '\');
        stepsup = 4;
        newpath = fullpath(1:allseps(end-stepsup)-1); %%% move two steps up in the path directory to get bath to the main animal folder (e.g. Z:/People/Nathan/Data/NH004 instead of Z:/People/Nathan/Data/NH004/160316/summed)
        cd(newpath)
        
        %%%%% Identify imaging field number
        currentimagingfield = gui_CaImageViewer.NewSpineAnalysisInfo.CurrentImagingField;
        
        %%% Identify instance of appearance of this imaging field (i.e. is this the first time imaging here? the second? etc.) 
        prompt = 'What imaging instance (of this field) is this?';
        name = 'Designate imaging instance';
        numlines = 1;
        ImageNum = get(gui_CaImageViewer.figure.handles.Frame_EditableText, 'String');
        defaultanswer = {ImageNum};
        
        currentsession = inputdlg(prompt, name, numlines, defaultanswer);
        currentsession = str2num(currentsession{1});
        
        try
            load([drawer, '_Imaging Field ', num2str(currentimagingfield), ' Spine Registry'])
            SRfound = 1;
        catch
            SRfound = 0;
        end
        
        if isempty(gui_CaImageViewer.NewSpineAnalysisInfo.SpineList)
            gui_CaImageViewer.NewSpineAnalysisInfo.SpineList(1:length(a.SpineROIs)-1) = ones(length(a.SpineROIs)-1,1);
        end

        if currentsession == 1 && ~SRfound
           SpineRegistry.Data(1:length(a.SpineROIs)-1,currentsession) = gui_CaImageViewer.NewSpineAnalysisInfo.SpineList;
           a.SpineStatusList = gui_CaImageViewer.NewSpineAnalysisInfo.SpineList;
        else  %% ZL comment: this part causing more issues in saving ROIs for session 1, use with caution
            SpineRegistry.Data(1:length(gui_CaImageViewer.NewSpineAnalysisInfo.SpineList),currentsession) = gui_CaImageViewer.NewSpineAnalysisInfo.SpineList;
            gui_CaImageViewer.NewSpineAnalysisInfo.SpineList(SpineRegistry.Data(:,currentsession) == 0) = 0;
            a.SpineStatusList = gui_CaImageViewer.NewSpineAnalysisInfo.SpineList;
        end
        save([drawer, '_Imaging Field ', num2str(currentimagingfield), ' Spine Registry'], 'SpineRegistry');
else
    global zStack_Interface
    if ishandle(zStack_Interface.figure)
        experiment = regexp(gui_CaImageViewer.filename, '[A-Z]{2,3}\d+', 'match');
        fname = [experiment{1}, '_zStackSavedROIs', '_DrawnBy', drawer];
    else
        experiment = regexp(gui_CaImageViewer.filename, '[A-Z]{2}\d+[_]\d+', 'match');
        if isempty(experiment)
            experiment{1} = gui_CaImageViewer.filename(1:end-4);
        end

        fname = [experiment{1}, '_SavedROIs', '_DrawnBy', drawer];
    end
end

if ~isempty(regexp(fname, ' '))
    fname = cell2mat(regexp(fname, ' ', 'split'));
end
eval([fname,'= a'])

target_dir = gui_CaImageViewer.save_directory;
cd(target_dir);

save(fname, fname)


% --------------------------------------------------------------------1:14
function User_DropDown_Callback(hObject, eventdata, handles)
% hObject    handle to User_DropDown (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


% --------------------------------------------------------------------
function ChangeUser_DropDown_Callback(hObject, eventdata, handles)
% hObject    handle to ChangeUser_DropDown (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


id = inputdlg('Enter new user name:', 'New User', 1);

set(handles.figure1, 'UserData', id{1})


% --------------------------------------------------------------------
function ImageOptions_DropDown_Callback(hObject, eventdata, handles)
% hObject    handle to ImageOptions_DropDown (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

global gui_CaImageViewer


% --------------------------------------------------------------------
function ColorMap_DropDown_Callback(hObject, eventdata, handles)
% hObject    handle to ColorMap_DropDown (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

global gui_CaImageViewer


% --------------------------------------------------------------------
function RGB_DropDown_Callback(hObject, eventdata, handles)
% hObject    handle to RGB_DropDown (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

global gui_CaImageViewer

gui_CaImageViewer.CurrentCMap = 'RGB';

if size(gui_CaImageViewer.ch1image,3)>1
    ch1image = gui_CaImageViewer.ch1image(:,:,2);
else
    ch1image = gui_CaImageViewer.ch1image;
end

PlaceImages(ch1image,[],'Slider');

% --------------------------------------------------------------------
function Jet_DropDown_Callback(hObject, eventdata, handles)
% hObject    handle to Jet_DropDown (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

global gui_CaImageViewer

gui_CaImageViewer.CurrentCMap = 'Jet';

if size(gui_CaImageViewer.ch1image,3)>1
    ch1image = gui_CaImageViewer.ch1image(:,:,2);
else
    ch1image = gui_CaImageViewer.ch1image;
end

PlaceImages(ch1image,[],'Slider');

% --------------------------------------------------------------------
function Hot_DropDown_Callback(hObject, eventdata, handles)
% hObject    handle to Hot_DropDown (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

global gui_CaImageViewer

gui_CaImageViewer.CurrentCMap = 'Hot';

if size(gui_CaImageViewer.ch1image,3)>1
    ch1image = gui_CaImageViewer.ch1image(:,:,2);
else
    ch1image = gui_CaImageViewer.ch1image;
end

PlaceImages(ch1image,[],'Slider');

% --------------------------------------------------------------------
function Fire_DropDown_Callback(hObject, eventdata, handles)
% hObject    handle to Fire_DropDown (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

global gui_CaImageViewer

gui_CaImageViewer.CurrentCMap = 'Fire';

if size(gui_CaImageViewer.ch1image,3)>1
    ch1image = gui_CaImageViewer.ch1image(:,:,2);
else
    ch1image = gui_CaImageViewer.ch1image;
end

PlaceImages(ch1image,[],'Slider');



% --------------------------------------------------------------------
function GraphScaling_DropDown_Callback(hObject, eventdata, handles)
% hObject    handle to GraphScaling_DropDown (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


% --------------------------------------------------------------------
function Stretched_DropDown_Callback(hObject, eventdata, handles)
% hObject    handle to Stretched_DropDown (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

global gui_CaImageViewer

PlaceImages(gui_CaImageViewer.ch1image,[],'Stretcher');

% --------------------------------------------------------------------
function Square_Dropdown_Callback(hObject, eventdata, handles)
% hObject    handle to Square_Dropdown (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

global gui_CaImageViewer

PlaceImages(gui_CaImageViewer.ch1image,[],'Square');



function ROIoffset_EditableText_Callback(hObject, eventdata, handles)
% hObject    handle to ROIoffset_EditableText (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of ROIoffset_EditableText as text
%        str2double(get(hObject,'String')) returns contents of ROIoffset_EditableText as a double


% --- Executes during object creation, after setting all properties.
function ROIoffset_EditableText_CreateFcn(hObject, eventdata, handles)
% hObject    handle to ROIoffset_EditableText (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in AveProjection_CheckBox.
function AveProjection_CheckBox_Callback(hObject, eventdata, handles)
% hObject    handle to AveProjection_CheckBox (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of AveProjection_CheckBox

global gui_CaImageViewer
global zStack_Interface

val = get(handles.AveProjection_CheckBox, 'Value');

ImageNum = str2num(get(gui_CaImageViewer.figure.handles.Frame_EditableText, 'String'));
twochannels = get(gui_CaImageViewer.figure.handles.TwoChannels_CheckBox, 'Value');
filterwindow = str2num(get(gui_CaImageViewer.figure.handles.SmoothingFactor_EditableText, 'String'));
merged = get(gui_CaImageViewer.figure.handles.Merge_ToggleButton, 'Value');

if ishandle(zStack_Interface.figure)
    SliceFocus = regexp(zStack_Interface.CurrentSliceEdit.String, '[0-9]+_*', 'match');
    if zStack_Interface.LimittoSlice
        numslices = str2num(zStack_Interface.SlicesEdit.String);
        currentslice = str2double(SliceFocus{1});
        allmults = [currentslice:numslices:length(gui_CaImageViewer.GCaMP_Image)];       
        if isempty(find(allmults==ImageNum,1))
            [~, ind] = min(abs(allmults-ImageNum));
            ImageNum = allmults(ind);
        end
    else
        allmults = 1:length(gui_CaImageViewer.GCaMP_Image);
    end
    if length(SliceFocus)>1
        z_diff = str2double(SliceFocus{2})-str2double(SliceFocus{1});
    else
        z_diff = 0;
    end
end

if val
    set(handles.MaxProjection_CheckBox, 'Value', 0);
    if ishandle(zStack_Interface.figure)
        im = gui_CaImageViewer.GCaMP_Image(allmults);
    else
        im = gui_CaImageViewer.GCaMP_Image;
    end
    im = cat(3, im{:});
    immax = mean(im, 3);
    
    
    if twochannels
        if ishandle(zStack_Interface.figure)
            overlim = (allmults+z_diff>length(gui_CaImageViewer.GCaMP_Image));
            if any(overlim)
                allmults = allmults(~overlim);
            end
            Rim = gui_CaImageViewer.GCaMP_Image(allmults+z_diff);
        else
            Rim = gui_CaImageViewer.Red_Image;
        end
        Rim = cat(3,Rim{:});
        Rimmax = mean(Rim, 3);
    end
    
    
    if filterwindow
    
        channel1 = immax;
        if twochannels && ~merged
            channel2 = Rimmax;
        elseif twochannels && merged
            channel1 = repmat(double(channel1)/max(max(double(channel1))),[1 1 3]);
            channel1(:,:,1) = zeros(size(channel1,1), size(channel1,2));
            channel1(:,:,3) = zeros(size(channel1,1), size(channel1,2));
            channel1(:,:,1) = double(Rimmax)/max(max(double(Rimmax)));
            channel2 = [];
        else
            channel2 = [];
        end

        CommandSource = 'Slider';

        %%%%%%%%%
        PlaceImages(channel1,channel2, CommandSource);
        %%%%%%%%%
    
    else
        smoothing_green = filter2(ones(filterwindow, filterwindow)/filterwindow^2, immax);
        channel1 = smoothing_green;
        if twochannels  && ~merged
            smoothing_red = filter2(ones(filterwindow, filterwindow)/filterwindow^2, Rimmax);
            channel2 = smoothing_red;
        elseif twochannels && merged
            channel1 = repmat(double(channel1)/max(max(double(channel1))),[1 1 3]);
            channel1(:,:,1) = zeros(size(channel1,1), size(channel1,2));
            channel1(:,:,3) = zeros(size(channel1,1), size(channel1,2));
            smoothing_red = filter2(ones(filterwindow, filterwindow)/filterwindow^2, Rimmax);
            channel1(:,:,1) = double(smoothing_red)/max(max(double(smoothing_red)));
            channel2 = [];
        else
            channel2 = [];
        end

        CommandSource = 'Slider';

        %%%%%%%%%
        PlaceImages(channel1,channel2, CommandSource);
        %%%%%%%%%
    end
else
    channel1 = gui_CaImageViewer.GCaMP_Image{ImageNum};
    
    if twochannels && ~merged
        if ishandle(zStack_Interface.figure)
            channel2 = gui_CaImageViewer.GCaMP_Image{ImageNum+z_diff};
        else
            channel2 = gui_CaImageViewer.Red_Image{ImageNum};
        end
    elseif twochannels && merged
            channel1 = repmat(double(channel1)/max(max(double(channel1))),[1 1 3]);
            channel1(:,:,1) = zeros(size(channel1,1), size(channel1,2));
            channel1(:,:,3) = zeros(size(channel1,1), size(channel1,2));
            channel1(:,:,1) = double(gui_CaImageViewer.Red_Image{ImageNum})/max(max(double(gui_CaImageViewer.Red_Image{ImageNum})));
            channel2 = [];
    else
            channel2 = [];
    end
    
    PlaceImages(channel1, channel2, 'Slider');
    
    CaImageSlider(ImageNum);
end


% --------------------------------------------------------------------
function MultipleSessions_DropDown_Callback(hObject, eventdata, handles)
% hObject    handle to MultipleSessions_DropDown (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


% --------------------------------------------------------------------
function MultiSession_DropDown_Callback(hObject, eventdata, handles)
% hObject    handle to MultiSession_DropDown (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

global gui_CaImageViewer

animal = regexp(gui_CaImageViewer.save_directory, '[A-Z]{2,3}0*[0-9]*', 'match');
fileparts = regexp(gui_CaImageViewer.save_directory, '[A-Z]{2,3}0*[0-9]*', 'split');
directory = [fileparts{1}, animal{1}];

exp_folder = dir(directory);

numsessions = length(exp_folder)-2;

choice = listdlg('PromptString', 'Which type of projection do you want to use?', 'ListString', {'Average Projection', 'Max Projection'}, 'SelectionMode', 'single');

scrsz = get(0, 'ScreenSize');
OverSessionsFigure = figure('Position', scrsz, 'Name', ['Multiple Sessions Analysis of ', animal{1}], 'NumberTitle', 'off');
set(OverSessionsFigure, 'UserData', zeros(1,14));
h1 = waitbar(0, 'Loading images for session 1');

gui_CaImageViewer.NewSpineAnalysis = 1;

%%%%% Downsampled move folder names

user_folder = regexp(directory, ['People', filesep, '\[A-Z]\w*'], 'match'); foldersplit = regexp(user_folder{1}, filesep, 'split'); user = foldersplit{2};

switch user
    case 'Assaf'
        dwnsampfoldername = '\motion_corrected_tiffs\GFP\summed';
    otherwise
        dwnsampfoldername = '\summed';
end

for i = 3:length(exp_folder)
    cd(directory)
    if isfolder(exp_folder(i).name) && isempty(regexp(exp_folder(i).name, '[A-Z]*'))
        try
            path = [directory, '\', exp_folder(i).name, dwnsampfoldername];
            cd(path);
            a = dir(cd);
            for j = 3:length(a)
                if ~isempty(strfind(a(j).name, 'summed_50.tif'))
                    imagefile = a(j).name;
                    break
                end
            end
            fname = [path,'\',imagefile];
            CaImage_File_info = imfinfo(fname);
            timecourse_image_number = numel(CaImage_File_info);
            TifLink = Tiff(fname, 'r');
            h2 = waitbar(0, 'Loading image ');
            Green_Frame = 1;
            GCaMP_Image = {};
                for j = 1:timecourse_image_number
                    TifLink.setDirectory(j);
                    GCaMP_Image{1,Green_Frame} = TifLink.read();
                    Green_Frame = Green_Frame+1;
                    waitbar(Green_Frame/timecourse_image_number,h2,['Loading Image ', num2str(Green_Frame)]);
                end
                delete(h2)
            im = cat(3, GCaMP_Image{:});
            if choice == 1
                immean = mean(im,3);
            else
                immean = max(im, [], 3);
            end
            figure(OverSessionsFigure);
        %     subplot(2,round(numsessions/2), i-2)
            figpos = get(gcf, 'Position');
            xint = figpos(3)/7;
            yint = figpos(4)/2;
            if (i-2)/7 <= 1
                yrow = 1;
            else
                yrow = 0;
            end
            posmat = [1:7,1:7];
            axes('Position', [((posmat(i-2)-1)*xint+10)/figpos(3), (yint*(yrow)+150)/figpos(4), 250/figpos(3), 250/figpos(4)])
            A = imagesc(immean); colormap(fire); set(gca, 'XTick', [], 'YTick', [])
            set(A,'ButtonDownFcn', @HighLightAxis)
            set(A, 'UserData', (i-2));
            title(exp_folder(i).name)
            waitbar((i-2)/numsessions, h1, ['Loading images for session ', num2str(i-2)])
        catch
            continue
        end
    else
    end
end

%%% Run these variables before manually adding a button!
%        figpos = get(gcf, 'Position');
%        xint = figpos(3)/7;
%        yint = figpos(4)/2;


uicontrol('Style', 'pushbutton', 'String', 'Project to Analysis Window', 'FontSize', 12, 'Units', 'Normalized','Position', [0.4 0.925 0.2 0.05], 'CallBack', @ProjectToAnalysisWindow)
uicontrol('Style', 'pushbutton', 'String', 'Group Selected Imaging Fields', 'Units', 'Normalized', 'Position', [((5)*xint+10)/figpos(3) 0.925 250/figpos(3) 0.05], 'CallBack', @GroupImagingWindows) %%% Position over the 6th image window 
uicontrol('Style', 'text', 'String', 'Image Field Count:', 'Units', 'Normalized', 'Position', [((6)*xint+10)/figpos(3), 0.925-0.02, 125/figpos(3), 0.05], 'BackgroundColor', get(gcf, 'Color'))
uicontrol('Style', 'edit', 'String', '1', 'Units', 'Normalized', 'Position', [((6)*xint+10)/figpos(3)+125/figpos(3), 0.925, 125/figpos(3), 0.05])
uicontrol('Style', 'pushbutton', 'String', 'Tabulate spine lifetimes of selected field', 'Units', 'Normalized', 'Position', [(10)/figpos(3), 0.925, 250/figpos(3), 0.05], 'Callback', @TabulateSpineLifetimes)
uicontrol('Style', 'pushbutton', 'String', 'Deselect All Axes', 'Fontsize', 12, 'Units', 'Normalized', 'Position', [((6)*xint+10)/figpos(3), 0.05, 250/figpos(3), 0.05], 'Callback', @DeselectAxes)
uicontrol('Style', 'pushbutton', 'String', 'Compare Image Pair', 'Fontsize', 12, 'Units', 'Normalized', 'Position', [(10)/figpos(3), 0.05, 250/figpos(3), 0.05], 'Callback', @CompareImagePair)
uicontrol('Style', 'checkbox', 'String', 'Try image alignment?', 'Tag', 'Alignment_CheckBox', 'Units', 'Normalized', 'Position', [((2-1)*xint+10)/figpos(3), 0.05, 250/figpos(3), 0.05], 'BackgroundColor', get(gcf, 'Color'))

delete(h1)


% --------------------------------------------------------------------
function ImageIntegrity_DropDown_Callback(hObject, eventdata, handles)
% hObject    handle to ImageIntegrity_DropDown (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


% --------------------------------------------------------------------
function CheckMotionCorrection_DropDown_Callback(hObject, eventdata, handles)
% hObject    handle to CheckMotionCorrection_DropDown (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

global gui_CaImageViewer

for i = 2:length(gui_CaImageViewer.GCaMP_Image)
    pwc(1,i) = corr2(gui_CaImageViewer.GCaMP_Image{i},gui_CaImageViewer.GCaMP_Image{i-1});
end

scrsz = get(0, 'ScreenSize');

figure('NumberTitle', 'off', 'Name', 'Pairwise Image Correlation Over Timecourse', 'Position', [0.25*scrsz(3),0.25*scrsz(4), 0.5*scrsz(3), 0.5*scrsz(4)]);
subplot(2,2,[1,3]); plot(pwc, 'k')
xlabel('Frame (Downsampled)', 'FontSize', 14)
title('Pairwise Correlation', 'FontSize', 14);

cd(gui_CaImageViewer.save_directory)
alignfile = [gui_CaImageViewer.filename(1:end-6), 't'];
try
    load(alignfile);
catch
    disp('No ''t'' file found')
end

subplot(2,2,2);
try
    plot(t);
    tc_length = length(t);
catch
    animal = regexp(gui_CaImageViewer.filename, '[A-Z]{2,3}0*[0-9]*', 'match');
    animal = animal{1};
    date= regexp(gui_CaImageViewer.save_directory, '[0-9]{6}', 'match'); date = date{1};
    t = CheckMC(animal, date);
    plot(t);
    tc_length = length(t);
end

xlabel('Frame (Actual)', 'FontSize', 14)
title('Attempted drift correction')
legend('X', 'Y')
ylim([-110 110])

subplot(2,2,4)
plot(t(:,1), t(:,2), '.k')
ylabel('Y Correction')
xlabel('X Correction')
ylim([-110 110])
xlim([-110 110])

uicontrol(gcf, 'Style', 'pushbutton', 'String', {'Set end frame'}, 'Fontsize', 8, 'Units', 'Normalized', 'Position', [0.915 0.56 0.08 0.09], 'Callback', {@SetEndFrame,tc_length})
uicontrol(gcf, 'Style', 'pushbutton', 'String', {'Clip image '}, 'Fontsize', 8, 'Units', 'Normalized', 'Position', [0.005 0.45 0.08 0.2], 'Callback', {@ClipImageSeriesLength, length(gui_CaImageViewer.GCaMP_Image)})
uicontrol(gcf, 'Style', 'pushbutton', 'String', {'Cut frames'}, 'Fontsize', 8, 'Units', 'Normalized', 'Position', [0.915, 0.45 0.08 0.09], 'Callback', {@RemoveFrames})
set(gcf, 'ToolBar', 'figure')


% --- Executes on button press in Autoscale_CheckBox.
function Autoscale_CheckBox_Callback(hObject, eventdata, handles)
% hObject    handle to Autoscale_CheckBox (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of Autoscale_CheckBox


% --- Executes on button press in Merge_ToggleButton.
function Merge_ToggleButton_Callback(hObject, eventdata, handles)
% hObject    handle to Merge_ToggleButton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of Merge_ToggleButton

global gui_CaImageViewer

merged = get(handles.Merge_ToggleButton, 'Value');

Green_loc = gui_CaImageViewer.GreenGraph_loc;
Red_loc = gui_CaImageViewer.RedGraph_loc;

if merged
    set(handles.RedGraph, 'Visible', 'off')
    gui_CaImageViewer.GraphPlacement = [Green_loc(1), Green_loc(2), Green_loc(3)+(Red_loc(1)-(Green_loc(1)+Green_loc(3))+Red_loc(3)), Green_loc(4)];
    set(handles.GreenGraph, 'Units', 'normalized')
    figure(gui_CaImageViewer.figure.handles.figure1)
    axes(gui_CaImageViewer.figure.handles.GreenGraph);
    intergraphdistance = Red_loc(1)-(Green_loc(1)+Green_loc(3));
    set(handles.GreenGraph, 'Position', [Green_loc(1), Green_loc(2), Green_loc(3)+Red_loc(3)+intergraphdistance, Green_loc(4)]);
    ch1image = gui_CaImageViewer.ch1image;
    ch1image(:,:,1) = gui_CaImageViewer.ch2image(:,:,1);    %%% Set the Red channel (dimension 1) of the existing green channel (whose channel 1 matrix is currently populated by zeros) to get an overlay
    PlaceImages(ch1image, [], 'Slider');
else
    set(handles.RedGraph, 'Visible', 'on')
    figure(gui_CaImageViewer.figure.handles.figure1)
    axes(gui_CaImageViewer.figure.handles.GreenGraph);
    set(handles.GreenGraph, 'Position', [Green_loc(1), Red_loc(2), Red_loc(3), Red_loc(4)]);      %%% If an image using only 1 channel is already loaded, the "green" graph overlays the red, but the size of the original axes is maintained in the "red" graph.
    set(handles.RedGraph, 'Position', [Red_loc(1), Red_loc(2),  Red_loc(3), Red_loc(4)]);
    set(handles.MaxProjection_CheckBox, 'Value', 0)
    ch1image = gui_CaImageViewer.GCaMP_Image{1};
    ch2image = gui_CaImageViewer.Red_Image{1};
    PlaceImages(ch1image,ch2image, 'Slider');
end



% --- Executes on button press in InsertSpine_ToggleButton.
function InsertSpine_ToggleButton_Callback(hObject, eventdata, handles)
% hObject    handle to InsertSpine_ToggleButton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of InsertSpine_ToggleButton

global gui_CaImageViewer

insertOpt = get(gui_CaImageViewer.figure.handles.InsertSpine_ToggleButton, 'Value');

if insertOpt

%     targetdend = str2num(cell2mat(inputdlg('Insert spine on which dendrite?', 'Select Dendrite', 1, {'1'})));
% 
%     lastspineondend = cumsum(cell2mat(cellfun(@length, gui_CaImageViewer.SpineDendriteGrouping, 'uni', false)));
% 
%     insertedspine = lastspineondend(targetdend)+1;
%     gui_CaImageViewer.InsertPoint = insertedspine;
        
end

% 
% for i = lastspineondend(end):-1:insertedspine %%% Descending because increasing tags by 1, then finding the next in the series results in all ROIs after the target having the same value
%     set(AllROIs(i), 'Tag', ['ROI', num2str(i+1)])
%     AllROItext = findobj('Tag', ['ROI', num2str(i), ' Text']);
%     set(AllROItext, 'String', [num2str(i+1)]);
%     set(AllROItext, 'Tag', ['ROI', num2str(i+1), ' Text'])
%     if ~isnan(AllBackgrounds(i))
%         set(AllBackgrounds(i), 'Tag', ['BackgroundROI', num2str(i+1)]);
%     end
% end
%     
% ROImat = nan(1,length(gui_CaImageViewer.ROI)+1);
%     ROImat(1:lastspineondend(targetdend)+1) = gui_CaImageViewer.ROI(1:lastspineondend(targetdend)+1);
%     ROImat(insertedspine+2:end) = gui_CaImageViewer.ROI(insertedspine+1:end);
%     gui_Viewer.ROI = ROImat;
% BGROImat = nan(CaImage1,length(gui_CaImageViewer.BackgroundROI)+1);
%     BGROImat(1:insertedspine) = gui_CaImageViewer.BackgroundROI(1:insertedspine);
%     BGROImat(insertedspine+2:end) = gui_CaImageViewer.BackgroundROI(insertedspine+1:end);
%     gui_CaImageViewer.BackgroundROI = BGROImat;
%     


% --------------------------------------------------------------------
function LoadFullImageSeries_DropDown_Callback(hObject, eventdata, handles)
% hObject    handle to LoadFullImageSeries_DropDown (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


% --------------------------------------------------------------------
function MotionCorrected_DropDown_Callback(hObject, eventdata, handles)
% hObject    handle to MotionCorrected_DropDown (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

global gui_CaImageViewer

%%% Get file information %%%

if ispc
    cd('Z:\People\Nathan\Data')
elseif isunix 
    cd('/usr/local/lab/People/Nathan/Data')
end

%%% Initialize/reset parameters and settings when loading new file
set(gui_CaImageViewer.figure.handles.MaxProjection_CheckBox, 'Value', 0);
set(gui_CaImageViewer.figure.handles.AveProjection_CheckBox, 'Value', 0);
set(gui_CaImageViewer.figure.handles.ImageSlider_Slider, 'Enable', 'on');
set(gui_CaImageViewer.figure.handles.Merge_ToggleButton, 'Value', 0)

% [filename, pathname] = uigetfile('.tif');

pathstructure = regexp(gui_CaImageViewer.save_directory, filesep);

parentpath = gui_CaImageViewer.save_directory(1:pathstructure(end-1));

cd(parentpath) 

fname = [gui_CaImageViewer.save_directory, gui_CaImageViewer.filename];
ext = strfind(fname, '_summed_50.tif');
if ~isempty(ext)
    fname = fname(1:ext-1);
end

a = regexp(fname, '\w+00[0]*\d+_\d+', 'match');
parsefile = a{1}(1:end-4);
animal = regexp(fname, '[A-Z]{2,3}0*[0-9]*', 'match');
animal = animal{1};
fname = [parentpath,parsefile];
CaImage_File_info = imfinfo([fname,'_001_corrected.tif']);

D = dir(parentpath);
timecourse_image_number = 0;
for i = 1:length(D)
    if ~isempty(strfind(D(i).name, 'corrected.tif'))
        timecourse_image_number = timecourse_image_number + 1;
    else
    end
end
steps = timecourse_image_number*length(CaImage_File_info);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%% Set Image Properties %%%

gui_CaImageViewer.GCaMP_Image = [];
gui_CaImageViewer.Red_Image = [];

h = waitbar(0, 'Loading Image ');

Green_loc = gui_CaImageViewer.GreenGraph_loc;
Red_loc = gui_CaImageViewer.RedGraph_loc;
GreenImageNumber = 1;

for i = 1:timecourse_image_number
    imnum = sprintf('%03d',i);
    if i == 1 || i ==2 || i == timecourse_image_number  %%% Acquisition 1 is easily overwritten by an accidental double-click of the 'grab' button, and can therefore be a different length; thus, find the length of the first file, then establish the standard length of acqusition two (all others except the final should be this length).
        CaImage_File_info = imfinfo([fname,'_', imnum, '_corrected.tif']);
    else
    end
    allimages = read_tiff([fname, '_', imnum, '_corrected.tif'],1,1,CaImage_File_info);
    for j = 1:length(CaImage_File_info)
        gui_CaImageViewer.GCaMP_Image{1,GreenImageNumber} = allimages(:,:,j);
        waitbar(GreenImageNumber/((timecourse_image_number-1)*800),h,['Loading Image ', num2str(GreenImageNumber)]);
        GreenImageNumber = GreenImageNumber+1;
    end
end

close(h)

channel1 = gui_CaImageViewer.GCaMP_Image;
channel2 = gui_CaImageViewer.Red_Image;

CommandSource = 'Loader';

[~, ~] = PlaceImages(channel1, channel2, CommandSource);

imageserieslength = size(gui_CaImageViewer.GCaMP_Image, 2);
gui_CaImageViewer.imageserieslength = imageserieslength;

set(handles.ImageSlider_Slider, 'Value', 1);
set(handles.ImageSlider_Slider, 'Min', 1);
set(handles.ImageSlider_Slider, 'Max', imageserieslength);
set(handles.ImageSlider_Slider, 'SliderStep', [(1/(GreenImageNumber-1)) (32/(GreenImageNumber-1))]);  %%% The Slider Step values indicate the minor and major transitions, which should be represented by the desired transition as the numerator and the length of the series as the denominator
set(handles.Frame_EditableText, 'String', 1);
set(handles.SmoothingFactor_EditableText, 'String', '1');

set(gui_CaImageViewer.figure.handles.output, 'WindowButtonDownFcn', [])

gui_CaImageViewer.LoadedFile = 1;

% --------------------------------------------------------------------
function Raw_DropDown_Callback(hObject, eventdata, handles)
% hObject    handle to Raw_DropDown (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


% --------------------------------------------------------------------
function ShiftROIsBetweenSessions_DropDown_Callback(hObject, eventdata, handles)
% hObject    handle to ShiftROIsBetweenSessions_DropDown (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

%%% To use this code, you need a 2x3 matrix, the "warp matrix", that is
%%% dreived from motion correction between the two images. If you run
%%% the "Compare Image Pair" code from the "Multiple Sessions Analysis"
%%% window, or otherwise run the function ecc on two images, you can get
%%% this matrix as an output. The "directionality" of the transformationF
%%% should match; i.e. if you're moving the ROIs from session 2 to match
%%% session 1, then the transformation matrix should be derived from moving
%%% the session 2 image to the template of the session 1 image. 

% warpmatrix = [1.0056,-0.0555,76.16581; 0.0575,1.0269,-23.3092];

global gui_CaImageViewer

warpmatrix = gui_CaImageViewer.NewSpineAnalysisInfo.WarpMatrix;

drawtype = get(gui_CaImageViewer.ROI(1), 'Type');

axes(gui_CaImageViewer.figure.handles.GreenGraph);

switch drawtype
    case 'rectangle'
        ROIs_original = round(cell2mat(cellfun(@(x) x(1:4), get(gui_CaImageViewer.ROI),'uni', false)));
    case 'images.roi.ellipse'
        ROIs_original = round(cell2mat(cellfun(@(x) x.Center, arrayfun(@(x) get(x), gui_CaImageViewer.ROI, 'uni', false), 'uni', false)'));
        OriginalSemiAxes = cell2mat(cellfun(@(x) x.SemiAxes, arrayfun(@(x) get(x), gui_CaImageViewer.ROI, 'uni', false), 'uni', false)');
        OriginalRotationAngle = cell2mat(cellfun(@(x) x.RotationAngle, arrayfun(@(x) get(x), gui_CaImageViewer.ROI, 'uni', false), 'uni', false)');
        OriginalAspectRatio = cell2mat(cellfun(@(x) x.AspectRatio, arrayfun(@(x) get(x), gui_CaImageViewer.ROI, 'uni', false), 'uni', false)');
end

if isfield(gui_CaImageViewer, 'ROIother')
    for i = 1:length(gui_CaImageViewer.ROIother)
        OtherROIs_original{i} = round(cell2mat(cellfun(@(x) x.Position, arrayfun(@(x) get(x), gui_CaImageViewer.ROIother(i), 'uni', false), 'uni', false)'));
    end
    OtherROIs_original_center = round(cell2mat(cellfun(@(x) mean(x.Position), arrayfun(@(x) get(x), gui_CaImageViewer.ROIother, 'uni', false), 'uni', false)'));
end

ClearROIs('AssumeAll')

imsize = size(gui_CaImageViewer.ch1image,1);
c1 = uicontextmenu;

uimenu(c1, 'Label', 'Add Surround Background', 'Callback', @ModifyROI);
uimenu(c1, 'Label', 'Remove Surround Background', 'Callback', @ModifyROI);
uimenu(c1, 'Label', 'Set as eliminated', 'Callback', @CategorizeSpines);
uimenu(c1, 'Label', 'Set as active', 'Callback', @CategorizeSpines);


for i = 1:length(ROIs_original)
    tempim = zeros(imsize,imsize);
    tempim(ROIs_original(i,1), ROIs_original(i,2)) = 1;
    transpos = spatial_interp(double(tempim'), warpmatrix, 'linear', 'affine', [1:imsize], [1:imsize]);
    stats = regionprops(logical(transpos));
    ROInum = i-1;
    if isempty(stats)
        disp(['Could not auto shift ROI ', num2str(i)])
        gui_CaImageViewer.ROI(i) = drawellipse('Center', ROIs_original(i,:), 'SemiAxes', OriginalSemiAxes(i,:), 'RotationAngle', OriginalRotationAngle(i,:),...
            'AspectRatio', OriginalAspectRatio(i,:), 'Tag', ['ROI', num2str(ROInum)], 'Color', [0.2 0.4 0.9], 'HandleVisibility', 'on', 'Label', '', 'Linewidth', 1, 'FaceAlpha', 0);
        roiget = get(gui_CaImageViewer.ROI(ROInum+1));
        c = roiget.UIContextMenu;
        uimenu(c, 'Label', 'Add Surround Background', 'Callback', @ModifyROI);
        uimenu(c, 'Label', 'Remove Surround Background', 'Callback', @ModifyROI);
        uimenu(c, 'Label', 'Set as eliminated', 'Callback', @CategorizeSpines);
        uimenu(c, 'Label', 'Set as active', 'Callback', @CategorizeSpines);
        gui_CaImageViewer.ROIlistener{ROInum+1} = listener(findobj(gui_CaImageViewer.ROI(ROInum+1)), 'DeletingROI', @DeleteROI);
        addlistener(findobj(gui_CaImageViewer.ROI(ROInum+1)), 'ROIClicked', @DeclareROI)
        continue
    end
    newpos(i,1:2) = stats.Centroid;
    switch drawtype
        case 'rectangle'
            gui_CaImageViewer.ROI(i) = rectangle('Position', [round(newpos(i,1)),round(newpos(i,2)),ROIs_original(i,3), ROIs_original(i,4)], 'EdgeColor', [0.2 0.4 0.9], 'Curvature', [1 1],'Tag', ['ROI', num2str(ROInum)], 'ButtonDownFcn', {@DragROI, ROInum, 'HomeWindow'}, 'Linewidth', 1, 'UIContextMenu', c1);
        case 'images.roi.ellipse'
            gui_CaImageViewer.ROI(i) = drawellipse('Center', newpos(i,:), 'SemiAxes', OriginalSemiAxes(i,:), 'RotationAngle', OriginalRotationAngle(i,:),...
                'AspectRatio', OriginalAspectRatio(i,:), 'Tag', ['ROI', num2str(ROInum)], 'Color', [0.2 0.4 0.9], 'HandleVisibility', 'on', 'Label', '', 'Linewidth', 1, 'FaceAlpha', 0);
            roiget = get(gui_CaImageViewer.ROI(ROInum+1));
            c = roiget.UIContextMenu;
            uimenu(c, 'Label', 'Add Surround Background', 'Callback', @ModifyROI);
            uimenu(c, 'Label', 'Remove Surround Background', 'Callback', @ModifyROI);
            uimenu(c, 'Label', 'Set as eliminated', 'Callback', @CategorizeSpines);
            uimenu(c, 'Label', 'Set as active', 'Callback', @CategorizeSpines);
            gui_CaImageViewer.ROIlistener{ROInum+1} = listener(findobj(gui_CaImageViewer.ROI(ROInum+1)), 'DeletingROI', @DeleteROI);
            addlistener(findobj(gui_CaImageViewer.ROI(ROInum+1)), 'ROIClicked', @DeclareROI)

    end
end

if isfield(gui_CaImageViewer, 'ROIother')
    if ~isempty(gui_CaImageViewer.ROIother)
        axes(gui_CaImageViewer.figure.handles.RedGraph);
        for i = 1:length(OtherROIs_original)
            tempim = zeros(imsize,imsize);
            tempim(OtherROIs_original_center(i,1), OtherROIs_original_center(i,2)) = 1;
            transpos = spatial_interp(double(tempim'), warpmatrix, 'linear', 'affine', [1:imsize], [1:imsize]);
            stats = regionprops(logical(transpos));
            othernewpos(i,1:2) = stats.Centroid-OtherROIs_original_center(i,:);
            gui_CaImageViewer.ROIother(i) = drawfreehand('Position', [OtherROIs_original{i}(:,1)+othernewpos(i,1),OtherROIs_original{i}(:,2)+othernewpos(i,2)], 'Tag', ['ROIother', num2str(i)], 'FaceAlpha', 0, 'Color', 'm', 'HandleVisibility', 'on', 'Label', num2str(i), 'InteractionsAllowed', 'all', 'Label', '');
    %         roiget = get(gui_CaImageViewer.ROIother(ROInum+1));
        end
    end
end

set(gui_CaImageViewer.figure.handles.EditSpines_ToggleButton, 'Value', 1);



% --- Executes on button press in Longitudinal_CheckBox.
function Longitudinal_CheckBox_Callback(hObject, eventdata, handles)
% hObject    handle to Longitudinal_CheckBox (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of Longitudinal_CheckBox


% --- Executes on selection change in ROIColor_PopUpMenu.
function ROIColor_PopUpMenu_Callback(hObject, eventdata, handles)
% hObject    handle to ROIColor_PopUpMenu (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns ROIColor_PopUpMenu contents as cell array
%        contents{get(hObject,'Value')} returns selected item from ROIColor_PopUpMenu


global gui_CaImageViewer

ColorOptions = get(handles.ROIColor_PopUpMenu, 'String');
ColorSelection = get(handles.ROIColor_PopUpMenu, 'Value');
NewColor = ColorOptions{ColorSelection};

if strcmpi(NewColor, 'ROI Color')
    return
end

ROIs = findobj('Type', 'images.ROI.Ellipse', '-and', '-not', {'-regexp', 'Tag', 'Dendrite'}, '-and', '-not', {'-regexp', 'Tag', 'Background'});

for i = 1:length(ROIs)
    set(ROIs(i), 'Color', NewColor)
end


% --- Executes during object creation, after setting all properties.
function ROIColor_PopUpMenu_CreateFcn(hObject, eventdata, handles)
% hObject    handle to ROIColor_PopUpMenu (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on selection change in PolyColor_PopUpMenu.
function PolyColor_PopUpMenu_Callback(hObject, eventdata, handles)
% hObject    handle to PolyColor_PopUpMenu (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns PolyColor_PopUpMenu contents as cell array
%        contents{get(hObject,'Value')} returns selected item from PolyColor_PopUpMenu

global gui_CaImageViewer

ColorOptions = get(handles.PolyColor_PopUpMenu, 'String');
ColorSelection = get(handles.PolyColor_PopUpMenu, 'Value');
NewColor = ColorOptions{ColorSelection};

if strcmpi(NewColor, 'Poly Color')
    return
end

PolyROIs = findobj('Type', 'images.ROI.Ellipse', '-and', {'-regexp', 'Tag', 'Dendrite'}, '-and', '-not', {'-regexp', 'Tag', 'Background'});
PolyLine = findobj('Type', 'line', '-and', {'-regexp', 'Tag', 'Poly'});

for i = 1:length(PolyROIs)
    set(PolyROIs(i), 'Color', NewColor)
end

for i = 1:length(PolyLine)
    set(PolyLine(i), 'Color', NewColor)
end

% --- Executes during object creation, after setting all properties.
function PolyColor_PopUpMenu_CreateFcn(hObject, eventdata, handles)
% hObject    handle to PolyColor_PopUpMenu (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on selection change in LineWidth_PopUpMenu.
function LineWidth_PopUpMenu_Callback(hObject, eventdata, handles)
% hObject    handle to LineWidth_PopUpMenu (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: contents = cellstr(get(hObject,'String')) returns LineWidth_PopUpMenu contents as cell array
%        contents{get(hObject,'Value')} returns selected item from LineWidth_PopUpMenu


global gui_CaImageViewer

WidthOptions = get(handles.LineWidth_PopUpMenu, 'String');
WidthSelection = get(handles.LineWidth_PopUpMenu, 'Value');
NewWidth = WidthOptions{WidthSelection};

if strcmpi(NewWidth, 'Poly Color')
    return
end

ROIs = findobj('Type', 'images.ROI.Ellipse', '-and', '-not', {'-regexp', 'Tag', 'Dendrite'}, '-and', '-not', {'-regexp', 'Tag', 'Background'});

for i = 1:length(ROIs)
    set(ROIs(i), 'LineWidth', str2num(NewWidth))
end

% --- Executes during object creation, after setting all properties.
function LineWidth_PopUpMenu_CreateFcn(hObject, eventdata, handles)
% hObject    handle to LineWidth_PopUpMenu (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: popupmenu controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in ShowLabels_ToggleButton.
function ShowLabels_ToggleButton_Callback(hObject, eventdata, handles)
% hObject    handle to ShowLabels_ToggleButton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

global gui_CaImageViewer

ROIs = findobj('Type', 'images.ROI.Ellipse', '-and', '-not', {'-regexp', 'Tag', 'Dendrite'}, '-and', '-not', {'-regexp', 'Tag', 'Background'});

choice = get(handles.ShowLabels_ToggleButton, 'Value');

if choice 
    for i = 1:length(ROIs)
        roilabel = regexp(ROIs(i).Tag, '[0-9]*', 'match');
        ROIs(i).Label = roilabel{1};
    end
else
    for i = 1:length(ROIs)
        ROIs(i).Label = '';
    end
end


% --- Executes on button press in EditSpines_ToggleButton.
function EditSpines_ToggleButton_Callback(hObject, eventdata, handles)
% hObject    handle to EditSpines_ToggleButton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of EditSpines_ToggleButton

global gui_CaImageViewer

editopt = get(handles.EditSpines_ToggleButton, 'Value');

ROIs = findobj(gui_CaImageViewer.figure.handles.GreenGraph, 'Type', 'images.roi.ellipse', '-and', '-not', {'-regexp', 'Tag', 'Dendrite'});

if editopt
    for i = 1:length(ROIs)
        ROIs(i).InteractionsAllowed = 'all';
    end
else
   for i = 1:length(ROIs)
        ROIs(i).InteractionsAllowed = 'none';
    end 
end


% --- Executes on button press in EditDendrites_ToggleButton.
function EditDendrites_ToggleButton_Callback(hObject, eventdata, handles)
% hObject    handle to EditDendrites_ToggleButton (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of EditDendrites_ToggleButton

global gui_CaImageViewer

editopt = get(handles.EditDendrites_ToggleButton, 'Value');

ROIs = findobj(gui_CaImageViewer.figure.handles.GreenGraph, 'Type', 'images.roi.ellipse', '-and', {'-regexp', 'Tag', 'Dendrite'});

if editopt
    for i = 1:length(ROIs)
        ROIs(i).InteractionsAllowed = 'all';
    end
else
   for i = 1:length(ROIs)
        ROIs(i).InteractionsAllowed = 'none';
   end 
end



% --------------------------------------------------------------------
function LaunchZStackInterface_DropDown_Callback(hObject, eventdata, handles)
% hObject    handle to LaunchZStackInterface_DropDown (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

global gui_CaImageViewer
global zStack_Interface

scrsz = get(0, 'ScreenSize');

wdth = 0.25*scrsz(3);
height = 0.25*scrsz(4);

zStack_Interface.figure = figure('Name', 'zStack Interface', 'NumberTitle', 'off','Position', [(0.5*scrsz(3))-(wdth/2), (0.5*scrsz(4))-(height/2), wdth, height], 'Units', 'Normalized');
txtwdth = 0.215; txthght = 0.1; spacer = 0.01; editwdth = 0.215; edithght = 0.1; btnhght = 0.1;
zStack_Interface.SlicesText = uicontrol('Style', 'Text', 'Units', 'Normalized', 'Position',[0.1 0.85 txtwdth txthght], 'String', {'Slices/Stack:'});
zStack_Interface.SlicesEdit = uicontrol('Style', 'Edit', 'Units', 'Normalized', 'Position',[0.1+txtwdth+spacer, 0.87, editwdth, edithght], 'String', '1','KeyPressFcn', @setslicenum);

zStack_Interface.ImportROIsButton = uicontrol('Style', 'Pushbutton', 'Units', 'Normalized', 'Position', [0.1, 0.65, (txtwdth+editwdth+spacer)/2, btnhght], 'String', 'ImportROIs', 'Callback', @importROIs);
zStack_Interface.ClearROIListButton = uicontrol('Style', 'Pushbutton', 'Units', 'Normalized', 'Position', [0.1+((txtwdth+editwdth+spacer)/2)+spacer, 0.65, (txtwdth+editwdth+spacer)/2-spacer, btnhght], 'String', 'Clear List', 'Callback', @clearROIlist);

tblwdth = txtwdth+editwdth+spacer/2;
zStack_Interface.ROITable = uitable(zStack_Interface.figure,'units', 'normalized', 'Position', [0.1+spacer/2, 0.05, tblwdth, 0.65-0.05], 'data',zeros(1,2), 'ColumnName', {'ROI', 'Slice'}, 'CellSelectionCallback', @grabcurrentROI);
zStack_Interface.AssignROIButton = uicontrol('Style', 'Pushbutton','Units', 'Normalized', 'String', 'Assign ROI to Current Slice', 'Position', [0.9-0.3, 0.65-2*btnhght, 0.3, 2*btnhght], 'Callback', @assignROItoslice);

currentSlice = str2num(gui_CaImageViewer.figure.handles.Frame_EditableText.String);
zStack_Interface.CurrentSliceText = uicontrol('Style', 'Text', 'Units', 'Normalized', 'Position', [0.1 0.75 txtwdth txthght], 'String', {'Current Slice:'});
zStack_Interface.CurrentSliceEdit = uicontrol('Style', 'Edit', 'Units', 'Normalized', 'Position', [0.1+txtwdth+spacer 0.77 txtwdth txthght], 'String', currentSlice);

zStack_Interface.ExtractTraces = uicontrol('Style', 'Pushbutton', 'Units', 'Normalized', 'String', 'Extract Traces', 'Position', [0.9-0.3, 0.05, 0.3, 2*btnhght], 'Callback', @ExtractZStackTraces);


%%%% Navigation panel for projecting selected slices onto the
%%%% gui_CaImageViewer window

navpanel = uipanel('units', 'normalized', 'Position', [0.9-0.3, 0.65, 0.3, 0.97-0.65]);

zStack_Interface.LoadSubSeriesButton = uicontrol('style', 'pushbutton', 'parent', navpanel,'String', 'Load image file', 'units', 'normalized', 'Position', [0.125 0.6 0.75 0.3], 'Callback', @loadsubseries);
zStack_Interface.ViewSelectedSliceMoviesButton = uicontrol('Style', 'togglebutton', 'parent', navpanel, 'units', 'normalized', 'String', 'Show select slices', 'Position', [0.125 0.15 0.75 0.3], 'Callback', @ViewSelectSlices);
zStack_Interface.LimittoSlice = 0;

% zStack_Interface.AssigntoFrame


