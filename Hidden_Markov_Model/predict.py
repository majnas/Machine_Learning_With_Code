import os
import yaml
import argparse
from rich import print
import cv2
import utils
import create_dataset
from hmm import HMM



def main(args):
    with open(args.cfg, "r") as f:
        config_data = yaml.load(f, Loader=yaml.FullLoader)
    config = utils.Config(**config_data)
    
    #? Instantiate preprocessing object
    pp = utils.Preprocess(n_emission=config.n_emission)

    hmm_obj = HMM(n_state=config.n_state, n_emission=config.n_emission)
    hmm_obj.load()
    print(hmm_obj)

    status, sample = create_dataset.get_sample(img_path=args.img_path, n_observations=config.n_observations)
    if status:
        sample = pp.preprocess_single_sample(sample=sample)
        winner_class, state_vote = hmm_obj.predict(observations=sample["observations"])

        # Visualize image and prediction
        img = cv2.imread(args.img_path)
        cv2.putText(img, f"Prediction: {config.classes[winner_class]}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 2)
        cv2.putText(img, f"State_vote: {state_vote}", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 2)
        cv2.imshow(os.path.basename(args.img_path), img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--cfg', type=str, default='config.yaml', help='config.yaml path')
    parser.add_argument('-i', '--img_path', type=str, default='./dataset/test/square/non_ideal_square_0.png', help='path to circle to square png image')
    args = parser.parse_args()
    main(args)
