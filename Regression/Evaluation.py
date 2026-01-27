# Databricks notebook source
import mlflow
import numpy as np
from sklearn.metrics import r2_score, mean_squared_error

def main():
    # Retrieve run_id from Train task
    run_id = dbutils.jobs.taskValues.get(taskKey="Train", key="run_id")

    # Load model
    model = mlflow.pyfunc.load_model(f"runs:/{run_id}/model")

    # Load evaluation data
    eval_df = spark.table("dev_contoso.lakehouse_monitoring.train_data").toPandas()
    X = eval_df.drop("label", axis=1)
    y = eval_df["label"]

    # Predict
    preds = model.predict(X)

    # Compute metrics
    r2 = float(r2_score(y, preds))  # convert to python float
    rmse = float(np.sqrt(mean_squared_error(y, preds)))

    print(f"R2 Score: {r2}")
    print(f"RMSE: {rmse}")

    # PASS metrics to next task (Condition task)
    dbutils.jobs.taskValues.set(key="r2_score", value=r2)
    dbutils.jobs.taskValues.set(key="rmse", value=rmse)

    #  combined pass/fail flag
    passes = (r2 >= 0.5) and (rmse <= 5.0)

    # If/else treats non-numeric types as strings, so store explicit "true"/"false"
    dbutils.jobs.taskValues.set("passes", "true" if passes else "false")

if __name__ == "__main__":
    main()







# import mlflow
# from sklearn.datasets import fetch_california_housing
# from sklearn.metrics import r2_score

# def main():
#     # Load model from MLflow Model Registry (latest version)
#     model = mlflow.pyfunc.load_model(
#         model_uri="models:/california_rf_model/latest"
#     )

#     # Load data
#     data = fetch_california_housing(as_frame=True)
#     df = data.frame
#     X = df[data.feature_names]
#     y = df["MedHouseVal"]

#     # Predict
#     preds = model.predict(X)

#     print("R2 Score:", r2_score(y, preds))

# if __name__ == "__main__":
#     main()
