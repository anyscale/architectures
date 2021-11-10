## import things
import ray
import pandas as pd
from prophet import Prophet

## data pre-processing
df = pd.read_csv('emb-parallel/yellow_tripdata_2021-01.csv')
df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"] ).dt.date.astype("datetime64")
df= df[["tpep_pickup_datetime", "VendorID", "PULocationID"]]
df = df.rename(columns={"tpep_pickup_datetime":"ds", "VendorID":"y"})
df = df.groupby([df["ds"], df["PULocationID"]]).count().reset_index()
loc_list = df["PULocationID"].unique()


## ray connection
ray.init("anyscale://parallel", log_to_driver=False, runtime_env={"pip":["prophet"],"excludes":["yellow*"]})
@ray.remote
def fit_prophet(i):
    m = Prophet()
    m.fit(df[df["PULocationID"]==i])
    return m

## back pressure to limit the # of tasks in flight
result = []
max_tasks = 10 # specifying the max number of results
for i in loc_list:
    if len(result) > max_tasks:
        # calculating how many results should be available
        num_ready = len(result)-max_tasks
        # wait for num_returns to be equal to num_ready, ensuring the amount of task in flight is checked
        ray.wait(result, num_returns=num_ready)
    result.append(fit_prophet.remote(i))
ray.get(result)



    
