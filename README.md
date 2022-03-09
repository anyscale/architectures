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

If you would like to run the application and tests locally, use an environment variable to set `RUN_RAY_LOCAL` to `True`.  The command will initialize a Ray cluster on your local machine. If the environment variable is not set, the tests and applications will attempt to launch a Ray cluster in your Anyscale account.

`export RUN_RAY_LOCAL=True`

By default, the application will attempt to launch or connect to an Anyscale cluster with a name similar to `anyscale://app-{ANYSCALE_ENVIRONMENT}` or `anyscale://app-{ANYSCALE_ENVIRONMENT}-tests` where the `ANYSCALE_ENVIRONMENT` variable is set using an environment variable.  If no environment variable is set, the default is `dev`.  To use an existing Anyscale cluster, the cluster address can be references using the `ANYSCALE_ADDRESS` environment variable.

Then, you can run tests locally, on an existing Anyscale cluster, or on a new cluster by running the following commands:

* `pytest tests/remote_tests.py`
* `pytest tests/test_app.py`

And if you've forked the repo, you can try the CI:

* Set a Github secret called `AUTOMATION_CLI_TOKEN` with your Anyscale CLI token in it.
* Push a change to a branch and create a Pull Request.
* Navigate to Github Actions to see the job run.

Once you are done testing, remember to terminate any Anyscale cluster that was created as part of the CI process either using the Anyscale Console or CLI.

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

