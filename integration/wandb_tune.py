import ray
import os
from ray import tune
from ray.tune.integration.wandb import wandb_mixin
import wandb

@wandb_mixin
def train_fn(config):
    for i in range(10):
        loss = config["a"] + config["b"]
        wandb.log({"loss": loss})
    tune.report(loss=loss, done=True)

ray.init("anyscale://integrations",
        project_dir=".", 
        runtime_env={"pip":["wandb","ray[tune]"],
            "env_vars":{"WANDB_API_KEY":f"{os.environ['WANDB_API_KEY']}"},
            "excludes":["tests", "yello*"]})
tune.run(
    train_fn,
    config={
        # define search space here
        "a": tune.choice([1, 2, 3]),
        "b": tune.choice([4, 5, 6]),
        # wandb configuration
        "wandb": {
            "project": "Optimization_Project",
            "entity":"cgreer",
        }
    })


