import ray
import os
# This script demonstrates using Weights and Biases from Anyscale
import time



@ray.remote
def log_something():
    import logging
    import json_log_formatter

    formatter = json_log_formatter.JSONFormatter()

    json_handler = logging.FileHandler(filename='my-log.json')
    json_handler.setFormatter(formatter)

    logger = logging.getLogger('my_json')
    logger.addHandler(json_handler)
    logger.setLevel(logging.INFO)

    logger.info('Log from Anyscale', extra={'worker': 'hello'})
    logger.info('Log from Anyscale', extra={'worker': 'hello'})
    logger.info('Log from Anyscale', extra={'worker': 'hello'})
    logger.info('Log from Anyscale', extra={'worker': 'hello'})
    logger.info('Log from Anyscale', extra={'worker': 'hello'})
    logger.error('Log from Anyscale', extra={'worker': 'hello'})
    return "OK"

ray.init("anyscale://integrations",
        project_dir=".", 
        cluster_env="data-dog:8",
        update=True,
        runtime_env={
            "pip":["json-log-formatter"],
            "excludes":["tests", "yello*"]})

print(ray.get(log_something.remote()))
time.sleep(60)
