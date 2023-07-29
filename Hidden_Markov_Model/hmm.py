import operator
from typing import List
import numpy as np

class HMM:
    def __init__(self, n_state: int, n_emission: int) -> None:
        self.n_state = n_state
        self.n_emission = n_emission
        self.emission = {}
        self.pi = {i:1/n_state for i in range(n_state)}
        self.transition = {sA: {sB: 0 for sB in range(n_state)} for sA in range(n_state)}
        for sidx in range(n_state):
            self.transition[sidx][sidx]=1
        for state_idx in range(self.n_state):
            self.emission[state_idx] = {f"E{ne}":0 for ne in range(n_emission)}

    def fit(self, samples):
        for sample in samples:
            observations = sample["observations"]
            for ob in observations:
                self.emission[sample['label']][ob] += 1 
        
        for state_idx in range(self.n_state):
            totall = sum(self.emission[state_idx][key] for key in self.emission[state_idx])
            self.emission[state_idx] = {k:v/totall for k,v in self.emission[state_idx].items()}


    def predict(self, observations: List):
        n_observation = len(observations)
        observation_probabilities = {-1: self.pi}
        # print("self.pi", self.pi)
        # print("observation_probabilities", observation_probabilities)

        for current_observation_idx, observation in enumerate(observations):
            previous_observation_idx = current_observation_idx - 1
            for current_state_idx in range(self.n_state):
                previous_state_prob = []
                for previous_state_idx in range(self.n_state):
                    prior = observation_probabilities[previous_observation_idx][previous_state_idx]
                    trans = self.transition[previous_state_idx][current_state_idx]
                    emission = self.emission[current_state_idx][observation]
                    prob = prior * trans * emission
                    previous_state_prob.append(prob)

                if current_observation_idx not in observation_probabilities:
                    observation_probabilities[current_observation_idx] = {}
                observation_probabilities[current_observation_idx][current_state_idx] = max(previous_state_prob)

        # print("observation_probabilities", observation_probabilities)
        state_vote = {state_idx:0 for state_idx in range(self.n_state)}

        for observation_idx in range(n_observation):
            observation_probabilities_state = observation_probabilities[observation_idx]
            winner_state = max(observation_probabilities_state.items(), key=operator.itemgetter(1))[0]
            state_vote[winner_state] += 1

        winner_class = max(observation_probabilities_state.items(), key=operator.itemgetter(1))[0]
        return winner_class, state_vote
    
    def save(self, path: str = "model.npz"):
        if not path.endswith(".npz"):
            path += ".npz"
    
        np.savez(path, 
            n_state = self.n_state,
            n_emission = self.n_emission,
            emission = self.emission,
            pi = self.pi,
            transition = self.transition)

    def load(self, path: str = "model.npz"):
        data = np.load(path, allow_pickle=True)
        n_state = data["n_state"]
        n_emission = data["n_emission"]
        
        if (self.n_state!=n_state):
            print(f"n_state is incompatible {self.n_state} vs {n_state}")

        if (self.n_emission!=n_emission):
            print(f"n_emission is incompatible {self.n_emission} vs {n_emission}")

        self.emission = data["emission"]
        self.pi = data["pi"]
        self.transition = data["transition"]

    def __str__(self) -> str:
        msg = f"HMM Properties:\n"
        msg += f"n_state: {self.n_state}\n"
        msg += f"n_emission: {self.n_emission}\n"
        msg += f"pi: {self.pi}\n"
        msg += f"emission: {self.emission}\n"
        msg += f"transition: {self.transition}\n"
        return msg



