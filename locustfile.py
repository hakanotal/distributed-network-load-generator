from locust import FastHttpUser, task, constant_throughput
import locust.stats

locust.stats.CSV_STATS_INTERVAL_SEC = 1
locust.stats.CSV_STATS_FLUSH_INTERVAL_SEC = 10 


class TestUser(FastHttpUser):
    wait_time = constant_throughput(1)

    @task
    def service(self):
        self.client.get("/load_test")
