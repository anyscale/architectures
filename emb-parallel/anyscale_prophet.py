## import things
import os
import ray
import logging
import pandas as pd

# Note -- this solution works only in the AWS BYOC solution
# For fully-managed, access to S3 must be explicitly configured.


@ray.remote
class DataHolder:

    def fetch_data(self):
        print("Fetching taxi data from s3")
        df = pd.read_csv("https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2021-01.csv")
        df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"] ).dt.date.astype("datetime64")
        df= df[["tpep_pickup_datetime", "VendorID", "PULocationID"]]
        df = df.rename(columns={"tpep_pickup_datetime":"ds", "VendorID":"y"})
        df = df.groupby([df["ds"], df["PULocationID"]]).count().reset_index()
        loc_list = df["PULocationID"].unique()
        self.df_ref = ray.put(df)
        print("Stored data in plasma store, returning list of locations to caller")
        return loc_list
    def data(self):
        return self.df_ref

@ray.remote(num_cpus=0.25)
def fit_prophet(i):
    import boto3
    from prophet import Prophet
    m = Prophet()
    holder = ray.get_actor("dataHolder", namespace="prophet")
    data_ref = ray.get(holder.data.remote())
    df = ray.get(data_ref)
    selection = df[df["PULocationID"]==i]
    if (len(selection) > 1):
        m.fit(selection)
        futures = m.make_future_dataframe(periods=30)
        forecast = m.predict(futures)
        forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_csv(f"s3://anyscale-jobs-cld-f2eq16c8ir2hsikddsvnmciq/taxi-prophet-data/output/forecast-{i}.csv")
    else:
        print("Not enough data for predictions")
    return f"done-with-{i}"


## back pressure to limit the # of tasks in flight
@ray.remote
def handle_runs():
    result = []
    max_tasks = 6 # This number should keep everything on one node
    holder = DataHolder.options(name="dataHolder", namespace="prophet").remote()
    loc_list = ray.get(holder.fetch_data.remote())
    for i in loc_list:
        if len(result) > max_tasks:
            # calculating how many results should be available
            num_ready = len(result)-max_tasks
            # wait for num_returns to be equal to num_ready, ensuring the amount of task in flight is checked
            ray.wait(result, num_returns=num_ready)
        result.append(fit_prophet.remote(i))
    
    for model in result:
        m = ray.get(model)
        print(m)

    
ray.init("anyscale://parallel-managed",
        cloud="anyscale-managed-2",
        log_to_driver=True,
        configure_logging=True,  # this is default
        logging_level=logging.DEBUG,
        runtime_env= {"pip":["prophet", "mlflow", "boto3","fsspec","s3fs"],"excludes":["yellow*"],
                "working_dir":".",
                "env_vars":{"MLFLOW_TRACKING_URI":"databricks",
                        "DATABRICKS_HOST":os.environ["DATABRICKS_HOST"],
                        "DATABRICKS_TOKEN":os.environ["DATABRICKS_TOKEN"],
                        "MLFLOW_EXPERIMENT_NAME":os.environ["MLFLOW_EXPERIMENT_NAME"]}},
        namespace="prophet")

ref = handle_runs.remote()

final_runs = ray.get(ref)

print(final_runs)




