# Databricks notebook source
# Upgrade Databricks SDK to the latest version and restart Python to see updated packages
%pip install --upgrade databricks-sdk==0.70.0 --quiet
%restart_python

from databricks.sdk.service.jobs import JobSettings as Job 


new_job = Job.from_dict(
    {
        "name": "Test_job1",
        "tasks": [
            {
                "task_key": "Training",
                "notebook_task": {
                    "notebook_path": "/Workspace/Users/sachin.kumar@snp.com/Training",
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
                    "notebook_path": "/Workspace/Users/sachin.kumar@snp.com/Evaluation",
                    "source": "WORKSPACE",
                },
                "existing_cluster_id": "1124-094650-0nervcma",
            },
        ],
        "queue": {
            "enabled": True,
        },
    }
)

from databricks.sdk import WorkspaceClient

w = WorkspaceClient()
result=w.jobs.create(**new_job.as_shallow_dict())
print("Created Job ID:", result.job_id)
# or create a new job using: w.jobs.create(**Test_job.as_shallow_dict())

run = w.jobs.run_now(job_id=result.job_id)
print("Run started:", run.run_id)




# COMMAND ----------

