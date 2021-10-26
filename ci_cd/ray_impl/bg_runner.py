from anyscale.background import run
# bg_job is a BackgroundJob object
bg_jobs = []
for n in range(4):
    bg_job = run("python remote_compute.py", address=f"anyscale://ci_cd_architecture{n}")
    bg_jobs.append(bg_job)
    bg_job.client_context.disconnect()
    





