import time
import os
import ray
from ray import tune
from ray.tune.integration.mlflow import mlflow_mixin
import json

@mlflow_mixin
def train_fn(config):
    for i in range(10):
        loss = config["a"] + config["b"]
    tune.report(loss=loss, done=True)

ray.init(
        "anyscale://integrations",
        project_dir=".", 
        runtime_env={"pip":["mlflow","ray[tune]"],
            "env_vars":{"MLFLOW_TRACKING_URI":"databricks",
                        "DATABRICKS_HOST":os.environ["DATABRICKS_HOST"],
                        "DATABRICKS_TOKEN":os.environ["DATABRICKS_TOKEN"],
            "excludes":["tests", "yello*"]})

tune.run(
    train_fn,
    config={
        # define search space here
        "a": tune.choice([1, 2, 3]),
        "b": tune.choice([4, 5, 6]),
        "mlflow":{
            "tracking_uri":"databricks",
            "experiment_name":os.environ["MLFLOW_EXPERIMENT_NAME"],
            "save_artifact":True
        }
    })

time.sleep(5)
