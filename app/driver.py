import ray
import time
import random
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
        """Fetch the results from the remote task.
        If the results are not yet ready, return just those that are, quickly.  Once all results are ready, return them all.
        """
        job_id = self.jobs[0]   #TODO handle multiple jobs
        status_info = self.client.get_job_status(job_id)
        status = status_info.status
        if (status == JobStatus.SUCCEEDED):
            return self.client.get_job_logs(job_id)
        if (status == JobStatus.FAILED):
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
