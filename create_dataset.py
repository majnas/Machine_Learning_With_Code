import os
import cv2
import glob
import numpy as np
import random

DATASET_DIR = "./dataset"
N = 10
points = []
labels = []
for class_id, class_name in enumerate(["circle", "square"]):
# for class_id, class_name in enumerate(["square"]):
# for class_id, class_name in enumerate(["circle"]):
    for img_path in glob.glob(os.path.join(DATASET_DIR, class_name, "*.png")):
        img = cv2.imread(img_path)  # Read image
        gray = cv2.cvtColor(img.copy(),cv2.COLOR_BGR2GRAY)

        # Setting parameter values
        t_lower = 10  # Lower Threshold
        t_upper = 250  # Upper threshold

        # Applying the Canny Edge filter
        edge = cv2.Canny(gray, t_lower, t_upper)

        contours = cv2.findContours(edge, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        try:
            if contours:
                points_ = contours[0][0].reshape(-1,2)
                point_idxs = np.linspace(0, points_.shape[0], N+1)[:-1]
                point_idxs = list(map(int, point_idxs))
                points_ = points_[point_idxs]
                points.append(points_)
                labels.append(class_id)
        except:
            continue

        # for p in points_:
        #     cv2.circle(edge, p, 10, 255, 1)

        # cv2.imshow('edge', edge)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

np.savez("data.npz", points=points, labels=labels)

