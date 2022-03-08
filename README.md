# architectures

Architectural Patterns for Ray and Anyscale Enablement.

This project holds configuration and code to demonstrate a basic application architecture and lifecycle that utilizes Anyscale for computation.

See (Anyscale Docs)[https://docs.anyscale.com/architectures/ci_cd] for documentation related to this repository.

## CI/CD 

To use it yourself, you'll need an Anyscale account.

* Clone the repo (or better yet, fork it)
* install the requirements `pip install -r app/ray_impl/requirements.txt`
* Use pip to install the local package `pip install -e .`
* Initialize this directory as a project in your own account: `anyscale project create`

Then, you can run tests

* `pytest tests/remote_tests.py`
* `pytest tests/test_app.py`

And if you've forked the repo, you can try the CI:

* Set a Github secret called `AUTOMATION_CLI_TOKEN` with your Anyscale CLI token in it.
* Push a change to a branch and create a PR.
* Navigate to Github Actions to see the job run.

## emb-parallel

This directory has example code for executing parallel tasks with Ray using prophet.  It also contains a complete example for running Prophet with cloud data on Anyscale.

To run in Anyscale, 
 
`python emb-parallel/anyscale_prophet.py`

Note, this script runs on a Anyscale AWS, EC2-base cluster; for the fully managed system, you'll need to setup AWS bucket access.

## integrations

This directory contains some sample code for integrating Ray on Anyscale with

* Weights and Biases
* DataDog
* MLFlow

Note that these scripts require various environment variables to be set in order to run.  In order to leverage any one of these patterns you have to create accounts on third-party services and configure appropriately.

