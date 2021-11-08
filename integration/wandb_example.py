import ray
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
        wandb.log({"loss": i})
        time.sleep(1)


ray.init("anyscale://integrations",
        project_dir=".", 
        runtime_env={"excludes":["tests", "yello*"]})
ray.get(log_to_wandb.remote())
#wandb.watch(model)
