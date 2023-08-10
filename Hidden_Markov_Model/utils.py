import os
from rich import print
import numpy as np
import math


"""
A class that represents a configuration object.

Attributes:
    * Any attributes that are passed to the `__init__` method.

Methods:
    * Any methods that are needed to access or modify the attributes of the object.
"""

class Config:
    def __init__(self, **kwargs):
        """
        Initializes a Config object.

        Args:
            * Any attributes that are passed to the `__init__` method.
        """

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        """
        Prints all attributes each in a separate line.
        """

        string = ""
        for key, value in self.__dict__.items():
            string += f"{key}: {value}\n"
        return string




class Preprocess:
    """
    Preprocessing class for extracting observations and preparing samples for Hidden Markov Model (HMM) training.

    Attributes:
        n_emission (int): Number of possible emissions (quantized angle differences).

    Methods:
        __init__(n_emission): Initialize the Preprocess object with the specified number of emissions.
        extract_observations(sample): Extract angle differences from a sample's points.
        quantize_observation(features): Quantize a list of features into emissions.
        preprocess_single_sample(sample): Preprocess a single sample by extracting observations and quantizing them.
        __call__(data_path): Load data and preprocess samples from the specified data path.
    """
    def __init__(self, n_emission: int = 10) -> None:
        """Initialize the Preprocess object."""
        self.n_emission = n_emission

    def extract_observations(self, sample):
        """
        Extract angle differences from a sample's points.

        Args:
            sample (dict): Sample data containing "points" as an array of points.

        Returns:
            list: List of angle differences between adjacent points.
        """
        sample_points = sample["points"]
        
        # Add first point to the end of array
        sample_points = np.concatenate((sample_points, sample_points[0:1]))
        n_points = len(sample_points)
        
        #? Calculate the angle of each point regarding the next point
        angles = []
        for i in range(1,n_points):
            x0,y0 = sample_points[i-1]
            x1,y1 = sample_points[i]
            angle = math.atan2(y1-y0, x1-x0) * 180 / np.pi
            if angle < 0:
                angle += 360
            angles.append(angle)

        diff_angles = []
        angles = np.concatenate((angles, angles[0:1]))
        for i in range(1,n_points):
            diff_angle = angles[i-1] - angles[i]
            if diff_angle < 0:
                diff_angle += 360

            if diff_angle > 180:
                diff_angle -= 180

            diff_angles.append(diff_angle)
        return diff_angles


    def quantize_observation(self, features):
        """
        Quantize a list of features into emissions.

        Args:
            features (list): List of numerical features (angle differences).

        Returns:
            list: List of quantized emissions.
        """
        emmision_span = 180 // self.n_emission + 1
        features = [f"E{int(f // emmision_span)}" for f in features]
        return features
    
    def preprocess_single_sample(self, sample):
        """
        Preprocess a single sample by extracting observations and quantizing them.

        Args:
            sample (dict): Sample data containing "points" and "label".

        Returns:
            dict: Preprocessed sample with "observations" and "label".
        """
        observations = self.extract_observations(sample)
        observations = self.quantize_observation(observations)
        return {"observations": observations, "label": sample["label"]}


    def __call__(self, data_path: str = None):
        """
        Load data and preprocess samples from the specified data path.

        Args:
            data_path (str, optional): Path to the data file. Defaults to None.

        Returns:
            None
        """
        data = np.load(data_path, allow_pickle=True)

        self.raw_train_samples = []
        for points, label in zip(data["points_train"], data["labels_train"]):
            self.raw_train_samples.append({"points": points, "label": label})

        self.raw_test_samples = []
        for points, label in zip(data["points_test"], data["labels_test"]):
            self.raw_test_samples.append({"points": points, "label": label})

        self.train_samples = [self.preprocess_single_sample(sample) for sample in self.raw_train_samples]
        np.random.shuffle(self.train_samples)
        self.test_samples = [self.preprocess_single_sample(sample) for sample in self.raw_test_samples]

if __name__ == "__main__":
    pp = Preprocess("./dataset/data.npz")
    pp.preprocess()
    print(pp.train_samples)
