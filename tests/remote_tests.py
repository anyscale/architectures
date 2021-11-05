import os
from app.ray_impl.remote_compute import sub_job, JobRunner
from app.driver import RayEntryPoint
import ray
import json
import sys

def setup_module():
    print(sys.path)
    ANYSCALE_URL="anyscale://tests"
    entry_point = RayEntryPoint(ANYSCALE_URL)

def test_sub_job():
    refs = [sub_job.remote() for i in range(10)]
    for r in refs:
        n = ray.get(r)
        assert n.number > -1 and n.number < 1 

def test_job_runner():
    j = JobRunner.remote()
    random_numbers = ray.get(j.do_something.remote())
    assert len(random_numbers) == 10
    ray.get(random_numbers) # cleanup

