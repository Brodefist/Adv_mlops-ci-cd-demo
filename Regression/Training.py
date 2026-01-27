# Databricks notebook source
# Databricks notebook: 02_Train_Model

import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestRegressor
from mlflow.models import infer_signature

def main():
    mlflow.set_experiment("/Shared/my_experiment")

    with mlflow.start_run() as run:
        # Load data from Unity Catalog
        train_df = spark.table("dev_contoso.lakehouse_monitoring.train_data").toPandas()

        X = train_df.drop("label", axis=1)
        y = train_df["label"]

        # Train model
        model = RandomForestRegressor()
        model.fit(X, y)

        # Log model artifact ONLY (no registration here)
        signature = infer_signature(X, model.predict(X))

        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="model",
            signature=signature,
            input_example=X.head(1)
        )
        #mlflow.sklearn.log_model(model, artifact_path="model")

        # Get run id so next task can evaluate + register
        run_id = run.info.run_id
        print("Training completed & model logged.")
        print("Run ID:", run_id)

        # Pass run_id to next task
        dbutils.jobs.taskValues.set(key="run_id", value=run_id)

if __name__ == "__main__":
    main()













# import mlflow
# import mlflow.sklearn
# from sklearn.datasets import fetch_california_housing
# from sklearn.ensemble import RandomForestRegressor

# def main():
#     mlflow.set_experiment("/Shared/my_experiment")

#     with mlflow.start_run():
#         # Load data
#         data = fetch_california_housing(as_frame=True)
#         df = data.frame
#         X = df[data.feature_names]
#         y = df["MedHouseVal"]

#         # Train
#         model = RandomForestRegressor()
#         model.fit(X, y)

#         # Log model to MLflow & register it
#         mlflow.sklearn.log_model(
#             sk_model=model,
#             artifact_path="model",
#             registered_model_name="california_rf_model"
#         )

# if __name__ == "__main__":
#     main()
