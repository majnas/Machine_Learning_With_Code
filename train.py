import os
import yaml
import argparse
from rich import print
from sklearn.metrics import accuracy_score, confusion_matrix

import utils
import create_dataset
from hmm import HMM

def main(args):
    with open(args.cfg, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    print(config)

    data_path = os.path.join(config["dataset_dir"], "data.npz")
    pp = utils.Preprocess(data_path=data_path, n_emission=config["n_emission"])
    pp()

    hmm_obj = HMM(n_state=config["n_state"], n_emission=config["n_emission"])
    hmm_obj.fit(samples=pp.train_samples)
    print(hmm_obj)

    # hmm_obj.save()
    # hmm_obj.load()
    # print(hmm_obj)

    y_pred = []
    y_true = []
    for sample in pp.test_samples:
        winner_class, state_vote = hmm_obj.predict(observations=sample["observations"])
        y_pred.append(winner_class)
        y_true.append(sample["label"])
        # print("pred_class", winner_class, "gt_class", sample["label"])

    acc = accuracy_score(y_true=y_true, y_pred=y_pred)
    print(f"accuracy={acc}")

    cm = confusion_matrix(y_true=y_true, y_pred=y_pred)
    print(f"confusion matrix=\n{cm}")
    

    # img_path = "./dataset/test/square/non_ideal_square_0.png"
    # status, sample = create_dataset.get_sample(img_path=img_path, n_observations=config["n_observations"])
    # if status:
    #     sample = pp.call_single_sample(sample=sample)
    #     winner_class, state_vote = hmm_obj.predict(observations=sample["observations"])
    #     print("pred_class", winner_class, "gt_class", sample["label"], "state_vote", state_vote)
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--cfg', type=str, default='config.yaml', help='config.yaml path')
    args = parser.parse_args()
    main(args)
