import os
import ray
from ray import tune
from ray.tune.integration.mlflow import MLflowLoggerCallback
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
                        "DATABRICKS_HOST":"https://dbc-073b287d-29d2.cloud.databricks.com",
                        "DATABRICKS_TOKEN":"dapi077fda433f7717096386f660d74db3aa"},
            "excludes":["tests", "yello*"]})

tune.run(
    train_fn,
    config={
        # define search space here
        "a": tune.choice([1, 2, 3]),
        "b": tune.choice([4, 5, 6]),
        "mlflow":{
            "tracking_uri":"databricks",
            "experiment_name":"/Users/cgreer@anyscale.com/first-experiment",
        }
    })
