class HMM:
    def __init__(self, samples, n_state: int, n_emission: int) -> None:
        self.samples = samples
        self.n_state = n_state
        self.n_emission = n_emission        
        self.emission = {}
        self.pi = {0: 0.5, 1:0.5}

        for ns in range(self.n_state):
            self.emission[ns] = {f"E{ne}":0 for ne in range(n_emission)}


    def calculate_emission_probabilities(self):
        for sample in self.samples:
            observations = sample["observations"]
            for ob in observations:
                self.emission[sample['label']][ob] += 1 

