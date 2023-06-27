import os
import math
import numpy as np


class Preprocess:
    def __init__(self, data_path: str, n_emission: int = 10) -> None:
        data = np.load(data_path, allow_pickle=True)
        self.n_emission = n_emission
        self.raw_train_samples = []
        for points, label in zip(data["points_train"], data["labels_train"]):
            self.raw_train_samples.append({"points": points, "label": label})

        self.raw_test_samples = []
        for points, label in zip(data["points_test"], data["labels_test"]):
            self.raw_test_samples.append({"points": points, "label": label})

    def extract_observations(self, sample):
        sample_points = sample["points"]
        
        # Add first to the end of array
        sample_points = np.concatenate((sample_points, sample_points[0:1]))
        n_points = len(sample_points)
        
        degrees = []
        for i in range(1,n_points):
            x0,y0 = sample_points[i-1]
            x1,y1 = sample_points[i]
            degree = math.atan2(y1-y0, x1-x0) * 180 / np.pi
            if degree < 0:
                degree += 360
            degrees.append(degree)

        diff_degrees = []
        degrees = np.concatenate((degrees, degrees[0:1]))
        for i in range(1,n_points):
            diff_degree = degrees[i-1] - degrees[i]
            if diff_degree < 0:
                diff_degree += 360

            if diff_degree > 180:
                diff_degree -= 180

            diff_degrees.append(diff_degree)
        return diff_degrees


    def quantize_observation(self, features):
        emmision_span = 180 // self.n_emission + 1
        features = [f"E{int(f // emmision_span)}" for f in features]
        return features
    
    def call_single_sample(self, sample):
        observations = self.extract_observations(sample)
        observations = self.quantize_observation(observations)
        return {"observations": observations, "label": sample["label"]}


    def __call__(self):
        self.train_samples = [self.call_single_sample(sample) for sample in self.raw_train_samples]
        np.random.shuffle(self.train_samples)
        self.test_samples = [self.call_single_sample(sample) for sample in self.raw_test_samples]

if __name__ == "__main__":
    pp = Preprocess("./dataset/data.npz")
    pp.preprocess()
    print(pp.train_samples)
