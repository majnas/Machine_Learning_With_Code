import os
import cv2
import glob
import numpy as np
import yaml
import argparse
from rich import print
import utils
import tqdm

def get_sample(img_path: str, n_observations: int=8, label=-1):
    img = cv2.imread(img_path)  # Read image

    gray = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY) # Convert to grayscale

    # Setting parameter values
    t_lower = 10  # Lower Threshold
    t_upper = 250  # Upper threshold

    # Applying the Canny Edge filter
    edge = cv2.Canny(gray, t_lower, t_upper)

    # Find contours for each sample
    contours = cv2.findContours(edge, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    try:
        if contours:
            contour_points = contours[0][0].reshape(-1,2)
            # Get index of n = n_observations points from all countour points
            point_idxs = np.linspace(0, contour_points.shape[0], n_observations+1)[:-1]
            point_idxs = list(map(int, point_idxs))
            selected_contour_points = contour_points[point_idxs]
    except:
        return False, None

    # #? To visualize points on sample
    # # Visualize all countour points in blue
    # # for p in contour_points:
    # #     cv2.circle(img, p, 5, (255, 0, 0), -1)

    # # Visualize all countour points in red
    # for p in selected_contour_points:
    #     cv2.circle(img, p, 5, (0, 0, 255), -1)

    # cv2.imshow('img', img)
    # # cv2.imwrite("img.png", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return True, {"points": selected_contour_points, "label": label}



def main(args):
    with open(args.cfg, "r") as f:
        config_data = yaml.load(f, Loader=yaml.FullLoader)
    config = utils.Config(**config_data)

    points = {"train": [], "test": []}
    labels = {"train": [], "test": []}
    for class_id, class_name in enumerate(["circle", "square"]):
        for part in ["train", "test"]:
            img_path_list = glob.glob(os.path.join(config.dataset_dir, part, class_name, "*.png"))
            for img_path in tqdm.tqdm(img_path_list, desc=f"{class_name} {part} part: "):
                status, sample = get_sample(img_path=img_path, n_observations=config.n_observations)
                if status:
                    points[part].append(sample["points"])
                    labels[part].append(class_id)

    data_path = os.path.join(config.dataset_dir, "data.npz")
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

