from locust import LoadTestShape
import numpy as np

spawn_rate = 100
time_limit = 60


class TestShape(LoadTestShape):
    
    def __init__(self):
        self.dist = np.genfromtxt('results/dist.csv', delimiter=',')

    def calculate_user(self, t):
        return self.dist[round(t)]

    def tick(self):
        run_time = self.get_run_time()

        if run_time < time_limit:
            user_count = self.calculate_user(run_time)
            return (user_count, spawn_rate)

        return None