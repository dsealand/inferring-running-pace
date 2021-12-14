"""
Converts output of OpenPose (.json) to a .txt file.
creat_db.py is required to be run after this script to merge all text files into format required for RNN for Human Activity Recognition - 2D Pose Input
Created by Stuart Eiffert 13/12/2017
All code is provided under the MIT License
"""


import json
from pprint import pprint
import glob, os

#Data path assumes that data is in format as ~/data/HAR_pose_activities/boxing/l01_c01_s01_a04_r01/pose, where boxing is replaced with whatever activity your pointing to
data_path = "running_dataset/results/"
activity_list =["5mph","6mph","7mph","8mph","9mph","10mph","11mph","12mph"]

# Currently set up to convert all camera clusters, subjects, activities and repetitions at the same time. 
#Note: Only 1 camera per cluster is being used
cluster_nums=4
camera_nums=1
subject_nums=12
activity_nums=8
repetition_nums=5

openpose_2person_count = 0

#loop through all saved .json files, outputs from Openspose
# for cluster in range(1,cluster_nums+1):
# 	for camera in range(1,camera_nums+1):
# 		for subject in range(1,subject_nums+1):
# 			subject_num = "0"+str(subject)
# 			#Because 10 doesnt have a 0 before it...
# 			if subject > 9:
# 				subject_num = str(subject)
# 			for camera in range(1,camera_nums+1):
for activity in range(0,activity_nums):					
    # for repetition in range(1,repetition_nums+1):
    # frame_set = "l0"+str(cluster)+"_c0"+str(camera)+"_s"+subject_num+"_a0"+str(activity)+"_r0"+str(repetition)
    # frame_set = str(activity)
    pose_kp_path = os.path.join(data_path,activity_list[activity])
    print(os.getcwd())
    #the below frames don't exist
    # if ((frame_set == "l03_c01_s05_a02_r05") or (frame_set == "l04_c01_s05_a02_r05")):
    #     continue
    if pose_kp_path != "running_dataset/results/5mph":
        os.chdir("../../../"+pose_kp_path)
    else:
        os.chdir(pose_kp_path)

    #kps is a list of pose keypoints in each frame, where kps[0] is the x position of kp0, kps[1] is the y position of kp0 etc
    kps = []
    #[kps.append([]) for i in range(36)]
    #loop through all .json files (1 per frame) in frameset. generally <140
    for file in sorted(glob.glob("*.json")):
        with open(file) as data_file: 
            data = json.load(data_file)
            #keep track of how often Openpose messes up and detects 2 people in the scene
            # print(data["people"][0]["pose_keypoints_2d"])							
            if data["people"][0]["person_id"]==-1:
                pprint("More than one detection in file, check the noise:")
                openpose_2person_count += 1
                print(file)
            frame_kps = []
            pose_keypoints = data["people"][0]["pose_keypoints_2d"]
            #loop through 25 pose keypoints (total = 75, 25x3 (x, y and accuracy))
            j = 0
            for i in range(50):
                frame_kps.append(pose_keypoints[j])
                j += 1
                if ((j+1) % 3 == 0):
                    j += 1
            kps.append(frame_kps)

    #Now we have kps, a list of lists, that includes the x and y positions of all 25 keypoints, for all frames in the frameset
    # So a list of length frameset.length, with each element being a 50 element long list.
    #Next, we simply loop through kps, writing the contents to a text file, where each sub list is a new line.
    #At this point, there is no overlap, and datasets are all of varying length
    # os.chdir(os.path.join(data_path,activity_list[activity]))
    output_file = activity_list[activity]+".txt"
    with open(output_file, "w") as text_file:
        for i in range(len(kps)):
            for j in range(50):
                text_file.write('{}'.format(kps[i][j]))
                if j < 49:
                    text_file.write(',')
            text_file.write('\n')

print(openpose_2person_count)