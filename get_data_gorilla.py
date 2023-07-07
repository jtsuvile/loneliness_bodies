import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2 

home_dir = '/Users/juusu53/Documents/projects/forte/questionnaire/'
data_dir = os.path.join(home_dir, 'data')
destination_folder = os.path.join(home_dir, 'processed_data')
maps = ['loneliness','connection']

task_dict = {'loneliness': '1-1',
             'connection': '2-1'}

#NB: have not checked if these sides are correct
which_side = {'activation': 'canvas_paint-',
             'deactivation': '--'}

# walk the directory
folders = [f.name for f in os.scandir(data_dir) if f.is_dir()]
print(folders)
#folders = ['data_exp_132396-v6_8883280'] 

for folder in folders:
    sub_folder = os.path.join(data_dir, folder, 'uploads')
    subid = folder.split('-')[1].split('_')[1]
    files = os.listdir(sub_folder)
    print(subid)
    # print(files)

    # TODO: figure out which task is which wave
    wave = 'task-7rcy'

    files_in_wave = [s for s in files if wave in s]

    if not files_in_wave:
        print(f"no files for sub {subid} wave {wave}")
        continue
    else:
        print(files_in_wave)

    for map_name in maps:
        if map_name == 'loneliness':
            activation_code = which_side.get('activation') + task_dict.get('loneliness') 
            deactivation_code = which_side.get('deactivation') + task_dict.get('loneliness') 
        elif map_name == 'connection':
            activation_code = which_side.get('activation') + task_dict.get('connection') 
            deactivation_code = which_side.get('deactivation') + task_dict.get('connection') 
        else:
            raise ValueError('map_name only defined for loneliness and connection, your input is' + map_name)

        file_to_read = [s for s in files_in_wave if activation_code in s]
        filepath = os.path.join(sub_folder, file_to_read[0])

        file_to_read2 = [s for s in files_in_wave if deactivation_code in s]
        filepath2 = os.path.join(sub_folder, file_to_read2[0])

        activations = cv2.imread(filepath)
        deactivations = cv2.imread(filepath2)

        act_color = np.array([0, 255, 0]).astype(int)
        mask_act = cv2.inRange(activations, act_color-50, act_color+50)
        mask_act[mask_act > 1] = 1
        
        deact_color = np.array([255, 0, 0]).astype(int)
        mask_deact = cv2.inRange(deactivations, deact_color-50, deact_color+50)
        mask_deact = mask_deact * -1
        mask_deact[mask_deact < -1] = -1

        combine = mask_deact + mask_act

        fig, ax = plt.subplots(figsize=(5.9,5.9))
        im = ax.imshow(combine,  cmap='coolwarm')
        fig.colorbar(im, ax=ax)
        plt.title(map_name)
        outfilename = f"{subid}_{map_name}_{wave}.jpg"
        print(outfilename)
        fig.savefig(os.path.join(destination_folder, outfilename), dpi=300)


print('done')
