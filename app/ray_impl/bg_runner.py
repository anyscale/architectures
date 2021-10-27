import ray
from anyscale.background import run
# bg_job is a BackgroundJob object
ray.init()
bg_jobs = []

@ray.remote
def launch(n):
    bg_job = run("python remote_compute.py", address=f"anyscale://ci_cd_architecture-r{n}")
    bg_job.client_context.disconnect()
    return bg_job

for n in range(3):
    bg_job = launch.remote(n)
    bg_jobs.append(bg_job)
    print(bg_jobs)

ray.get(bg_jobs)
    





