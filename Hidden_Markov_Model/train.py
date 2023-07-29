import os
import yaml
import argparse
from rich import print
from sklearn.metrics import accuracy_score, confusion_matrix
import utils
from hmm import HMM



def main(args):
    with open(args.cfg, "r") as f:
        config_data = yaml.load(f, Loader=yaml.FullLoader)
    config = utils.Config(**config_data)
    print(config)

    data_path = os.path.join(config.dataset_dir, "data.npz")
    pp = utils.Preprocess(n_emission=config.n_emission)
    pp(data_path=data_path)

    hmm_obj = HMM(n_state=config.n_state, n_emission=config.n_emission)
    hmm_obj.fit(samples=pp.train_samples)
    hmm_obj.save()
    print(hmm_obj)

    y_pred = []
    y_true = []
    for sample in pp.test_samples:
        winner_class, state_vote = hmm_obj.predict(observations=sample["observations"])
        y_pred.append(winner_class)
        y_true.append(sample["label"])

    acc = accuracy_score(y_true=y_true, y_pred=y_pred)
    print(f"accuracy={acc}")

    cm = confusion_matrix(y_true=y_true, y_pred=y_pred)
    print(f"confusion matrix=\n{cm}")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--cfg', type=str, default='config.yaml', help='config.yaml path')
    args = parser.parse_args()
    main(args)
