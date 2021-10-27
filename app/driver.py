import ray
import time
import random

from .ray_impl.remote_compute import JobRunner

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
            ray.init(url, 
                    project_dir=".", 
                    runtime_env={"excludes":["tests"]}
                    # this is one place to configure Anyscale environment
                    # if they do not vary by execution environment
                    #cluster_env=
                    #cluster_compute=
                    )
            self.actor = JobRunner.remote()
        self.initialized = True

    def execute(self):
        """Kicks off the remote job.
        Makes sure not to block with any calls to ray.get.
        """
        self.result_ref = self.actor.do_something.remote()

    def respond(self):
        """Fetch the results from the remote task.
        If the results are not yet ready, return just those that are, quickly.  Once all results are ready, return them all.
        """
        response = []
        try:
            results  = ray.get(self.result_ref, timeout=0.5)
            for x in results:
                try:
                    response.append(ray.get(x, timeout=0.5))
                except GetTimeoutError:
                    response.append(f"Not ready yet: {self.result_ref}")
                    return response
        except AttributeError:
            response.append(f"No job hes yet been submitted")
        except GetTimeoutError:
            response.append(f"Not ready yet: {self.result_ref}")
        return response

    def cleanup(self):
        ray.kill(self.actor)

if (__name__ == "__main__"):
    url = "anyscale://ci_cd_architecture"
    entry_point = RayEntryPoint(url)
    entry_point.execute()
    print(entry_point.respond())
    time.sleep(5)
    print(entry_point.respond())
