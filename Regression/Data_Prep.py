# Databricks notebook source
# Load raw data from Unity Catalog
df = spark.table("dev_contoso.lakehouse_monitoring.california_housing")

# Rename target column
df = df.withColumnRenamed("MedHouseVal", "label")

# Save processed data to new UC Delta table
df.write.mode("overwrite").saveAsTable("dev_contoso.lakehouse_monitoring.train_data")

print("Data prep completed: dev_contoso.lakehouse_monitoring.train_data created ✔")
