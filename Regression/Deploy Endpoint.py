# Databricks notebook source
import os
os.environ["DATABRICKS_HOST"] = "https://adb-7405617328913463.3.azuredatabricks.net//"
dbutils.widgets.text("model_name", "")
dbutils.widgets.text("model_version", "")

model_name = dbutils.widgets.get("model_name")
model_version = dbutils.widgets.get("model_version")

if not model_name or not model_name.strip():
    raise ValueError("model_name widget must be set and non-empty.")

import re

# Sanitize and build endpoint name
safe_model_name = re.sub(r'[^A-Za-z0-9_-]', '', model_name.strip())
endpoint_base = f"{safe_model_name}-prod-endpoint"
endpoint_name = re.sub(r'[^A-Za-z0-9]+$', '', endpoint_base[:63])

print(f"Deploying Model: {model_name} v{model_version}")
print(f"Endpoint name: {endpoint_name}")

from mlflow.deployments import get_deploy_client
from databricks.sdk.errors import NotFound
import time

client = get_deploy_client("databricks")

try:
    client.get_endpoint(endpoint_name)
    print("Updating existing endpoint...")
    client.update_endpoint(
    endpoint_name,
    {
        "served_models": [
            {
                "model_name": model_name,
                "model_version": int(model_version),
                "workload_type": "CPU",
                "workload_size": "Small"
            }
        ]
    }
)
    
except Exception as e:
    if "RESOURCE_DOES_NOT_EXIST" in str(e):
        print("Creating new endpoint...")
        client.create_endpoint(
            name=endpoint_name,
            config={
                "served_models": [{
                    "model_name": model_name,
                    "model_version": int(model_version),
                    "workload_type": "CPU",
                    "workload_size": "Small"
                }]
            }
        )
    else:
        raise


# except NotFound:
#     print("Creating new endpoint...")
#     client.create_endpoint(
#         name=endpoint_name,
#         config={
#             "served_models": [
#                 {
#                     "model_name": model_name,
#                     "model_version": int(model_version),
#                     "workload_type": "CPU",
#                     "workload_size": "Small"
#                 }
#             ]
#         }
#     )


print("Waiting for endpoint to be ready...")
time.sleep(10)

workspace_url = os.environ.get("DATABRICKS_HOST")
if not workspace_url:
    raise ValueError("DATABRICKS_HOST environment variable must be set to construct the endpoint URL.")

endpoint_url = f"{workspace_url}/serving-endpoints/{endpoint_name}/invocations"
dbutils.notebook.exit(f"Endpoint URL: {endpoint_url}")


# print(f"Endpoint URL: {endpoint_url}")
# print("Deployment complete!")
# time.sleep(10)


