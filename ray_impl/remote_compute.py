import ray
import time
import random
import json

class MyModel:
    def __init__(self, name, number):
        self.name = name
        self.number = number

    def as_json(self):
        return json.dumps({"name":self.name,"number":self.number})

@ray.remote
def sub_job():
    """A Ray task that generates random numbers within a typed structure."""
    time.sleep(5)
    return MyModel(random.choice(list("alongradomstring")), random.uniform(-1,1))


@ray.remote
class JobRunner:
    def do_something(self):
        random_numbers = []
        for i in range(10):
            random_numbers.append(sub_job.remote())
        return random_numbers

if (__name__ == "__main__"):
    ray.init("anyscale://ci_cd_architecture", project_dir="ray_impl")
    x = JobRunner.remote()
    r = x.do_something.remote()
    results_list = ray.get(r)
    print([ray.get(r2).as_json() for r2 in results_list])
