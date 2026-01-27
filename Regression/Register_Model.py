# Databricks notebook source
import mlflow

def main():
    # Get run_id passed from Train task
    run_id = dbutils.jobs.taskValues.get(taskKey="Train", key="run_id")
    print("Registering model from run:", run_id)

    model_name = "california_rf_model"

    # Register the model with MLflow Model Registry
    result = mlflow.register_model(
        model_uri=f"runs:/{run_id}/model",
        name=model_name
    )

    print(f"Model registered as: {model_name}")
    print(f"Version created: {result.version}")

    # Pass version forward if needed later
    dbutils.jobs.taskValues.set(key="model_name", value=model_name)
    dbutils.jobs.taskValues.set(key="model_version", value=result.version)
    

if __name__ == "__main__":
    main()
