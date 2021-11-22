import ray
import os
# This script demonstrates using Weights and Biases from Anyscale
import time

@ray.remote
def log_to_wandb():
    import wandb

    wandb.init(project="my-test-project", entity="cgreer")
    wandb.config = {
      "learning_rate": 0.001,
      "epochs": 100,
      "batch_size": 128
    }
    for i in range(100):
        wandb.log({"loss": i*i/10000})
        time.sleep(0.5)


ray.init("anyscale://integrations",
        project_dir=".", 
        runtime_env={"pip":["wandb"],
            "env_vars":{"WANDB_API_KEY":f"{os.environ['WANDB_API_KEY']}"},
            "excludes":["tests", "yello*"]})
ray.get(log_to_wandb.remote())
