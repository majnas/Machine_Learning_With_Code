import os
import yaml
import argparse
from rich import print

import utils
import hmm

def main(args):
    with open(args.cfg, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    print(config)

    data_path = os.path.join(config["dataset_dir"], "data.npz")
    pp_obj = utils.Preprocess(data_path=data_path, 
                              n_emission=config["n_emission"])
    pp_obj.preprocess()

    hmm_obj = hmm.HMM(samples=pp_obj.samples, 
                      n_state=config["n_state"], 
                      n_emission=config["n_emission"])
    hmm_obj.calculate_emission_probabilities()
    print(hmm_obj.emission)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--cfg', type=str, default='config.yaml', help='config.yaml path')
    args = parser.parse_args()
    main(args)
