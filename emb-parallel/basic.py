# import things
import pandas as pd
from prophet import Prophet

# data pre-processing
df = pd.read_csv('./yellow_tripdata_2021-01.csv')
df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"] ).dt.date.astype("datetime64")
df= df[["tpep_pickup_datetime", "VendorID", "PULocationID"]]
df = df.rename(columns={"tpep_pickup_datetime":"ds", "VendorID":"y"}).groupby([df["ds"], df["PULocationID"]]).count().reset_index()
loc_list = df["PULocationID"].unique()

# vanilla impl without ray
result = {}
for i in loc_list:
    m = Prophet()
    m.fit(df[df["PULocationID"]==i])
    result[i]=m 



# ray connection
ray.init()
@ray.remote
def fit_prophet(i):
    m = Prophet()
    m.fit(df[df["PULocationID"]==i])
    result[i]=m 

## Fire Hose Approach -- fire as fast as you can and wait for the result
result = []
for i in loc_list:
    result.append(fit_prophet.remote(i))
ray.get(result)


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



    
