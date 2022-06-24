import os
import pickle
import re
import time
from dataclasses import dataclass

from PyQt5.QtWidgets import QFileDialog


def output_data(parent):
    """Function to organize data output and save"""
    # make a few new attributes
    filename = parent.filename.split("/")[-1]
    mouse_id = re.search("[A-Z]{2}[0-9]{3}", parent.filename).group()
    ROI_ids = {}
    for key, value in parent.ROI_fluorescence.items():
        if key != "Dendrite Poly":
            ids = []
            for v in range(value.shape[1]):
                ids.append(f"{key} {v+1}")
        else:
            ids = []
            for i, dend in enumerate(value):
                dends = []
                for poly in range(dend.shape[1]):
                    dends.append(f"{key} {i} Poly {poly + 1}")
                ids.append(dends)
        ROI_ids[key] = ids

    ROI_flags = {}
    for key, value in parent.ROIs.items():
        flags = []
        for v in value:
            flags.append(v.flag)
        ROI_flags[key] = flags

    parent.parameters["Bout Separation Frames"] = parent.bout_separation_frames

    output = Activity_Output(
        filename=filename,
        mouse_id=mouse_id,
        parameters=parent.parameters,
        ROI_ids=ROI_ids,
        ROI_flags=ROI_flags,
        ROI_positions=parent.ROI_positions,
        fluorescence=parent.ROI_fluorescence,
        processed_fluorescence=parent.fluorescence_processed,
        drifting_baseline=parent.drifting_baseline,
        dFoF=parent.dFoF,
        processed_dFoF=parent.processed_dFoF,
        activity_trace=parent.activity_trace,
        floored_trace=parent.floored_trace,
        deconvolved_spikes=parent.deconvolved_spikes,
        spine_pixel_intensity=parent.spine_pixel_intensity,
        dend_segment_intensity=parent.dend_seg_intensity,
        spine_volume=parent.spine_volume,
        corrected_spine_pixel_intensity=parent.corrected_spine_pixel_intensity,
        corrected_dend_segment_intensity=parent.corrected_dend_seg_intensity,
        corrected_spine_volume=parent.corrected_spine_volume,
    )

    # save_name = QFileDialog.getSaveFileName(parent, "Save Output")[0]
    save_dialog = QFileDialog()
    # save_dialog.setOptions(QFileDialog.DontUseNativeDialog)
    save_dialog.setFileMode(QFileDialog.AnyFile)
    save_dialog.setAcceptMode(QFileDialog.AcceptSave)
    save_dialog.setDirectory(r"C:\Users\Jake\Desktop\Analyzed_data\individual")
    year = time.ctime(os.path.getctime(parent.filename))[-2:]
    mouse = re.search("JW[0-9]{3}", filename).group()
    date = year + re.search("[0-9]{4}", filename).group()
    sname = f"{mouse}_{date}_imaging_data"
    save_dialog.selectFile(sname)
    save_dialog.show()

    if save_dialog.exec() == QFileDialog.Accepted:
        save_name = save_dialog.selectedFiles()[0]
        pickle_name = save_name + ".pickle"
        with open(pickle_name, "wb") as f:
            pickle.dump(output, f)


@dataclass
class Activity_Output:
    """Dataclass for storing the final output of the Activity Viewer"""

    filename: str
    mouse_id: str
    parameters: dict
    ROI_ids: dict
    ROI_flags: dict
    ROI_positions: dict
    fluorescence: dict
    processed_fluorescence: dict
    drifting_baseline: dict
    dFoF: dict
    processed_dFoF: dict
    activity_trace: dict
    floored_trace: dict
    deconvolved_spikes: dict
    spine_pixel_intensity: list
    dend_segment_intensity: list
    spine_volume: list
    corrected_spine_pixel_intensity: list
    corrected_dend_segment_intensity: list
    corrected_spine_volume: list

