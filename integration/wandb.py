# This script demonstrates using Weights and Biases from Anyscale

import wandb

wandb.init(project="my-test-project", entity="grechaw")
wandb.config = {
  "learning_rate": 0.001,
  "epochs": 100,
  "batch_size": 128
}
wandb.log({"loss": loss})

# Optional
wandb.watch(model)

