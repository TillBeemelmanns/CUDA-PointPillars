"""
author: hova88
date: 2021/03/16
"""
import numpy as np
from visual_tools import draw_clouds_with_boxes
import open3d as o3d
import argparse
import os
import glob

parser = argparse.ArgumentParser()
parser.add_argument('--data_dir', type=str, default='/workspace/data', help='Directory containing .bin and .txt files')
parser.add_argument('--score_thr', type=float, default=0.1)
parser.add_argument('--verbose', action='store_true')
parser.add_argument('--draw_arrow', action='store_true')

if __name__ == "__main__":
    args = parser.parse_args()
    data_dir = args.data_dir
    score_thr = args.score_thr

    print("Score threshold:", score_thr)
    print("Data directory:", data_dir)

    bin_files = sorted(glob.glob(os.path.join(data_dir, '*.bin')))
    if not bin_files:
        print(f"No .bin files found in {data_dir}")
    else:
        for cloud_path in bin_files:
            boxes_path = cloud_path.replace('.bin', '.txt')
            if not os.path.exists(boxes_path):
                print(f"Warning: Corresponding .txt file not found for {cloud_path}, skipping.")
                continue
            
            print(f"\nVisualizing: {os.path.basename(cloud_path)}")

            cloud = np.fromfile(cloud_path, dtype=np.float32).reshape(-1,4)
            
            # Handle empty txt file
            if os.path.getsize(boxes_path) > 0:
                boxes = np.loadtxt(boxes_path).reshape(-1,9)
                boxes = boxes[boxes[:, -1] > score_thr][:, :7]
                classes = boxes[:, -2].astype(int)  # Second last column
            else:
                boxes = np.array([])
                classes = np.array([])

            draw_clouds_with_boxes(cloud, boxes, classes, draw_arrow=args.draw_arrow, verbose=args.verbose)