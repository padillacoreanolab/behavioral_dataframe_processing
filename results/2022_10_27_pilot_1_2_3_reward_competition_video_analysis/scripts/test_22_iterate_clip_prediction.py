#!/usr/bin/env python3

"""
"""

import os 
import pandas as pd

model_fullpath = "/nancy/projects/sleap_pose_tracking/results/2022_10_10_pilot_1_2_3_reward_competition_cd1/proc/round_3_test_22_23_34/models/baseline_medium_rf.bottomup"


cs_presentation_frame_df = pd.read_csv("/nancy/user/riwata/projects/behavioral_dataframe_processing/results/2022_10_27_pilot_1_2_3_reward_competition_video_analysis/proc/10-03-22_Test_22_6-1v6-3.mp4.cs_presentation_frame_numbers.csv")
for index, row in cs_presentation_frame_df.iterrows():
    os.makedirs(row["prediction_clip_output_dirname"], exist_ok=True)
    sleap_command = "sleap-track {} \
    --frames {}-{} \
    --tracking.tracker flow \
    --tracking.similarity centroid --tracking.match greedy \
    --tracking.clean_instance_count 2 \
    --tracking.target_instance_count 2 \
    -m {} \
    --output {}".format(row["video_full_path"], \
    row["10_seconds_before_cs_presentation_in_frame"], \
    row["10_seconds_after_cs_presentation_in_frame"], \
    model_fullpath,
    row["prediction_clip_output_full_path"])
    print(sleap_command)
    os.system(sleap_command)
