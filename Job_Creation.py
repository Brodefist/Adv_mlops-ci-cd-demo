# Databricks notebook source
# Upgrade Databricks SDK to the latest version and restart Python to see updated packages
%pip install --upgrade databricks-sdk==0.70.0 --quiet
%restart_python

from databricks.sdk import WorkspaceClient

# Define the job as a plain dictionary
new_job = {
    "name": "Test_job1",
    "tasks": [
        {
            "task_key": "Training",
            "notebook_task": {
                "notebook_path": "/Workspace/Users/sachin.kumar@snp.com/GitDeployment/Training"
                "source": "WORKSPACE",
            },
            "existing_cluster_id": "1124-094650-0nervcma",
        },
        {
            "task_key": "Evaluation",
            "depends_on": [
                {
                    "task_key": "Training",
                },
            ],
            "notebook_task": {
                "notebook_path": "/Workspace/Users/sachin.kumar@snp.com/GitDeployment/Evaluation"
                "source": "WORKSPACE",
            },
            "existing_cluster_id": "1124-094650-0nervcma",
        },
    ],
    "queue": {
        "enabled": True,
    },
}

w = WorkspaceClient()

# Create job using dict unpacking (**)
result = w.jobs.create(**new_job)
print("Created Job ID:", result.job_id)

# Trigger the run
run = w.jobs.run_now(job_id=result.job_id)
print("Run started:", run.run_id)
