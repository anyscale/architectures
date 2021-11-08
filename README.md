# architectures

Architectural Patterns for Ray and Anyscale Enablement.

This project holds configuration and code to demonstrate a basic application architecture and lifecycle that utilizes Anyscale for computation.

See (Anyscale Docs)[https://docs.anyscale.com/architectures/ci_cd] for documentation related to this repository.

To use it yourself, you'll need an Anyscale account.

* Clone the repo (or better yet, fork it)
* install the requirements `pip install -r app/ray_impl/requirements.txt`
* Use pip to install the local package `pip install -e .`
* Initialize this directory as a project in your own account: `anyscale init`

Then, you can run tests

* pytest tests/remote_test.py
* pytest tests/test_app.py

And if you've forked the repo, you can try the CI:

* Set a Github secret called `AUTOMATION_CLI_TOKEN` with your Anyscale CLI token in it.
* Push a change to a branch and create a PR.
* Navigate to Github Actions to see the job run.
