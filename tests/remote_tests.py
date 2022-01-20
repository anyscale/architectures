import os
from app.ray_impl.script import sub_task, TaskRunner
import ray
import json
import sys

def setup_module():
    print(sys.path)
    ANYSCALE_URL="anyscale://tests"
    ray.init(ANYSCALE_URL)

def test_sub_task():
    refs = [sub_task.remote() for i in range(10)]
    for r in refs:
        n = ray.get(r)
        assert n.number > -1 and n.number < 1 

def test_task_runner():
    j = TaskRunner.remote()
    random_numbers = ray.get(j.do_something.remote())
    assert len(random_numbers) == 10
    ray.get(random_numbers) # cleanup
