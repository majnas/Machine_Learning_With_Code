import os
import yaml
import argparse
from rich import print
import cv2
import utils
import create_dataset
from hmm import HMM



def main(args):
    """
    Main function to predict the class of an image using a trained Hidden Markov Model (HMM).

    Args:
        args (argparse.Namespace): Command-line arguments.

    Returns:
        None
    """
    with open(args.cfg, "r") as f:
        config_data = yaml.load(f, Loader=yaml.FullLoader)
    config = utils.Config(**config_data)
    
    #? Instantiate preprocessing object
    pp = utils.Preprocess(n_emission=config.n_emission)

    #? Load the trained HMM model
    hmm_obj = HMM(n_state=config.n_state, n_emission=config.n_emission)
    hmm_obj.load()
    print(hmm_obj)

    #? Get a sample image and preprocess it
    status, sample = create_dataset.get_sample(img_path=args.img_path, n_observations=config.n_observations)
    if status:
        sample = pp.preprocess_single_sample(sample=sample)
        winner_class, state_vote = hmm_obj.predict(observations=sample["observations"])

        #? Visualize image and prediction
        img = cv2.imread(args.img_path)
        cv2.putText(img, f"Prediction: {config.classes[winner_class]}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 2)
        cv2.putText(img, f"State_vote: {state_vote}", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 2)
        basename = os.path.basename(args.img_path)
        cv2.imshow(basename, img)
        file_name, extension = os.path.splitext(basename)
        img_path = file_name + "_pred" + extension
        cv2.imwrite(img_path, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    #? Command-line argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('--cfg', type=str, default='config.yaml', help='config.yaml path')
    parser.add_argument('-i', '--img_path', type=str, default='./dataset/test/square/non_ideal_square_0.png', help='path to circle to square png image')
    args = parser.parse_args()
    main(args)
