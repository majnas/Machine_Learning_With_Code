import operator
from typing import List
import numpy as np

class HMM:
    """
    Hidden Markov Model (HMM) for image classification using angle differences.

    Attributes:
        n_state (int): Number of states (classes) in the HMM.
        n_emission (int): Number of possible emissions (angle differences) in the HMM.
        emission (dict): Emission probabilities for each state and emission.
        pi (dict): Prior probabilities for each state.
        transition (dict): Transition probabilities between states.

    Methods:
        __init__(n_state, n_emission): Initialize the HMM with the specified number of states and emissions.
        fit(samples): Train the HMM using the provided training samples.
        predict(observations): Predict the state of a sequence of observations using the Viterbi algorithm.
        save(path): Save the trained HMM model to a file.
        load(path): Load a trained HMM model from a file.
        __str__(): Return a string representation of the HMM's properties.
    """
    def __init__(self, n_state: int, n_emission: int) -> None:
        """Initialize the Hidden Markov Model."""
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
        """Train the Hidden Markov Model using the provided training samples."""
        for sample in samples:
            observations = sample["observations"]
            for ob in observations:
                self.emission[sample['label']][ob] += 1 
        
        for state_idx in range(self.n_state):
            totall = sum(self.emission[state_idx][key] for key in self.emission[state_idx])
            self.emission[state_idx] = {k:v/totall for k,v in self.emission[state_idx].items()}


    def predict(self, observations: List):
        """
        Predict the state of a sequence of observations using the Viterbi algorithm.

        Args:
            observations (list): List of observations (angle differences) for prediction.

        Returns:
            tuple: A tuple containing the predicted state and a dictionary of state votes.
        """
        n_observation = len(observations)
        observation_probabilities = {-1: self.pi}
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
        """
        Save the trained Hidden Markov Model to a file.

        Args:
            path (str, optional): Path to save the model file. Defaults to "model.npz".
        """
        if not path.endswith(".npz"):
            path += ".npz"
        with open(path, 'wb') as file:
            np.savez_compressed(file,
                                n_state=self.n_state,
                                n_emission=self.n_emission,
                                emission=self.emission,
                                pi=self.pi,
                                transition=self.transition)

    def load(self, path: str = "model.npz"):
        """
        Load a trained Hidden Markov Model from a file.

        Args:
            path (str, optional): Path to the model file. Defaults to "model.npz".
        """
        with open(path, 'rb') as file:
            data = np.load(file, allow_pickle=True)
            n_state = data["n_state"]
            n_emission = data["n_emission"]
            
            if (self.n_state!=n_state):
                print(f"n_state is incompatible {self.n_state} vs {n_state}")

            if (self.n_emission!=n_emission):
                print(f"n_emission is incompatible {self.n_emission} vs {n_emission}")

            self.emission = data["emission"].item()
            self.pi = data["pi"].item() 
            self.transition = data["transition"].item()


    def __str__(self) -> str:
        """Return a string representation of the Hidden Markov Model's properties."""
        msg = f"HMM Properties:\n"
        msg += f"n_state: {self.n_state}\n"
        msg += f"n_emission: {self.n_emission}\n"
        msg += f"pi: {self.pi}\n"
        msg += f"emission: {self.emission}\n"
        msg += f"transition: {self.transition}\n"
        return msg



