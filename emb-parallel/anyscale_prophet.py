## import things
import os
import ray
import pandas as pd
from prophet import Prophet
import mlflow



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
        return loc_list
    def data(self):
        return self.df_ref

@ray.remote
def fit_prophet(i):
    m = Prophet()
    holder = ray.get_actor("dataHolder", namespace="prophet")
    data_ref = ray.get(holder.data.remote())
    df = ray.get(data_ref)
    selection = df[df["PULocationID"]==i]
    if (len(selection) > 1):
        m.fit(selection)
    mlflow.log_model("my_model",m)
    return m

## ray connection
ray.init("anyscale://parallel", log_to_driver=False, 
        runtime_env= {"pip":["prophet", "mlflow"],"excludes":["yellow*"],
                "env_vars":{"MLFLOW_TRACKING_URI":"databricks",
                        "DATABRICKS_HOST":os.environ["DATABRICKS_HOST"],
                        "DATABRICKS_TOKEN":os.environ["DATABRICKS_TOKEN"],
                        "MLFLOW_EXPERIMENT_NAME":os.environ["MLFLOW_EXPERIMENT_NAME"]}},
                        namespace="prophet")
#ray.init(log_to_driver=False, namespace="prophet")
## back pressure to limit the # of tasks in flight
result = []
max_tasks = 10 # specifying the max number of results
try:
    holder = ray.get_actor("dataHolder", namespace="prophet")
except:
    holder = DataHolder.options(name="dataHolder", namespace="prophet", lifetime="detached").remote()

loc_list = ray.get(holder.fetch_data.remote())
for i in loc_list:
    if len(result) > max_tasks:
        # calculating how many results should be available
        num_ready = len(result)-max_tasks
        # wait for num_returns to be equal to num_ready, ensuring the amount of task in flight is checked
        ray.wait(result, num_returns=num_ready)
    result.append(fit_prophet.remote(i))

result = ray.get(result)
ray.kill(holder)

for m in result:
    try:
        f = m.make_future_dataframe(periods=2)
    except Exception:
        print("One of the models has not been fit")
    print(f.tail())

print(result)



    
