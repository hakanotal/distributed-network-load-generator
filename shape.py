from locust import LoadTestShape
import numpy as np
import os

PATH = os.path.dirname(os.path.abspath(__file__))

spawn_rate = 10
time_limit = 60


class TestShape(LoadTestShape):
    
    def __init__(self):
        self.dist = np.genfromtxt(PATH + '/results/dist.csv', delimiter=',')
        # self.dist = np.arange(0, 60)


    def calculate_user(self, t):
        return self.dist[round(t)]

    def tick(self):
        run_time = self.get_run_time()

        if run_time < time_limit:
            user_count = self.calculate_user(run_time)
            return (user_count, spawn_rate)

        return None