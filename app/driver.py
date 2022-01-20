import ray
import time
import random
import click
from ray.dashboard.modules.job.sdk import JobSubmissionClient
from ray.dashboard.modules.job.common import JobStatus, JobStatusInfo



from ray.exceptions import GetTimeoutError

class RayEntryPoint:
    """A driver class that encapsulates interaction with the ray cluster.  On initialization, the cluster is created or connected.  A remote actor is also instantiated, which contains the remote methods that will be called via this entry point class
    """
    def __init__(self, url):
        self.initialized = False
        self.initialize(url)

    def initialize(self, url):
        if (not(self.initialized)):
            self.url = url
            self.jobs = []
            try:
                self.client = JobSubmissionClient(url)
            except click.exceptions.ClickException:
                # if the cluster is not running, Ray JobSubmissionClient cannot be created.
                ray.init(url)
                self.client = JobSubmissionClient(url)
        self.initialized = True

    def execute(self):
        """Kicks off the remote task.
        Makes sure not to block with any calls to ray.get.
        """
        job_id = self.client.submit_job(
            entrypoint="python app/ray_impl/script.py",
            # Working dir
            runtime_env={
                "working_dir": "./",
                "pip": ["requests==2.26.0"],
                "excludes":["tests"]
                }
            )
        self.jobs.append(job_id)

    def respond(self):
        """Fetch the results from a job.
        This naive approach always returns the status of the first-submitted job.
        If it is complete, it returns the results and pops that job off the stack.
        """
        if (len(jobs)==0):
            return "No Job Running"
        else:
            job_id = self.jobs[0]
            status_info = self.client.get_job_status(job_id)
            status = status_info.status
            if (status in {JobStatus.SUCCEEDED, JobStatus.FAILED}):
                jobs.pop(0)
                return self.client.get_job_logs(job_id)
            else:
                return status, job_id

    def cleanup(self):
        ray.kill(self.actor)

if (__name__ == "__main__"):
    url = "anyscale://tests"
    entry_point = RayEntryPoint(url)
    entry_point.execute()
    print(entry_point.respond())
    time.sleep(5)
    print(entry_point.respond())
