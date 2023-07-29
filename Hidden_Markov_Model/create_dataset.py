import os
import cv2
import glob
import numpy as np
import yaml
import argparse
from rich import print

def get_sample(img_path: str, n_observations: int=8):
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
            point_idxs = np.linspace(0, points_.shape[0], n_observations+1)[:-1]
            point_idxs = list(map(int, point_idxs))
            points_ = points_[point_idxs]
    except:
        return False, None

    # for p in points_:
    #     cv2.circle(edge, p, 10, 255, 1)

    # cv2.imshow('edge', edge)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return True, {"points": points_, "label": -1}



def main(args):
    with open(args.cfg, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    print(config)

    points = {"train": [], "test": []}
    labels = {"train": [], "test": []}
    for class_id, class_name in enumerate(["circle", "square"]):
        for part in ["train", "test"]:
            for img_path in glob.glob(os.path.join(config["dataset_dir"], part, class_name, "*.png")):
                status, points_ = get_sample(img_path=img_path, n_observations=config["n_observations"])
                if status:
                    points[part].append(points_["points"])
                    labels[part].append(class_id)

    data_path = os.path.join(config["dataset_dir"], "data.npz")
    np.savez(data_path, 
             points_train=points["train"],
             points_test=points["test"], 
             labels_train=labels["train"],
             labels_test=labels["test"],
             )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--cfg', type=str, default='config.yaml', help='config.yaml path')
    args = parser.parse_args()
    main(args)

