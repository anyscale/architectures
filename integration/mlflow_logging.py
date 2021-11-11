import os
import ray
import mlflow

import logging

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)


@ray.remote
def logging_task():
    with mlflow.start_run():
        alpha = "ALPHA"
        l1_ratio = "L1"
        rmse = 0.211
        r2 = 0.122
        mae = 30
        mlflow.log_param("alpha", alpha)
        mlflow.log_param("l1_ratio", l1_ratio)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("mae", mae)
    return "Done"

ray.init(
        "anyscale://integrations",
        #project_dir=".", 
        runtime_env={"pip":["mlflow","ray[tune]"],
            "env_vars":{"MLFLOW_TRACKING_URI":"databricks",
                        "DATABRICKS_HOST":"https://dbc-073b287d-29d2.cloud.databricks.com",
                        "DATABRICKS_TOKEN":os.environ["DATABRICKS_TOKEN"],
                        "MLFLOW_EXPERIMENT_NAME":os.environ["MLFLOW_EXPERIMENT_NAME"]},
            "excludes":["tests", "yello*"]})

print(ray.get(logging_task.remote()))
#print(logging_task())
