# Databricks notebook source
df = spark.table("dev_contoso.lakehouse_monitoring.train_data").toPandas()
X = df.drop("label", axis=1)
y = df["label"]

run_id = dbutils.jobs.taskValues.get("Train", "run_id")
model = mlflow.pyfunc.load_model(f"runs:/{run_id}/model")

preds = model.predict(X)

r2 = float(r2_score(y, preds))
rmse = float(np.sqrt(mean_squared_error(y, preds)))

dbutils.jobs.taskValues.set("passes", "true" if (r2 >= 0.5 and rmse <= 5.0) else "false")


# COMMAND ----------


