# XGBoost-Ray demo

This demo demonstrates an end to end machine learning workload using XGBoost training on a Ray cluster in Anyscale
 * Distributed data loading and pre-processing using Ray dataset.
 * The use of `RayXGBoost` as part of the [xgboost_ray project](https://github.com/ray-project/xgboost_ray)
 * Distributed training on Ray cluster
 * Distributed batch inference
 * Distributed feature importance 

## Instructions

### Step 1.
If you want to generate data in the current directory, create a `data` directory.
 ` mkdir data`

Before starting the demo, run `create_learnable_data.py -f ./data/classification.parquet`, specifying only the path. 
By default, `create_learnable_data.py` creates data in `~/data/classification.parquet`.

This step generates fake partitioned classification parquet data. Using all the defaults 
should suffice. To see all the arguments to this data generating utility, 
use `create_learnable_data.py --help`

### Step 2. 
Create a conda environment "conda create -n xgboost-demo python==3.8
Once you activate the environment (`conda activate xgboost-demo`), you will need to install ray and anyscale ) This example was tested using ray 1.9.2 (`pip install ray==1.9.2 anyscale`)
Launch the `jupyter notebook` on your laptop.  
Set the `data_path` variable in first cell in the `xgboost_demo.ipynb` to the path you used
above.

### Step 3.

Use the Ansycale cluster created for this demo:
 * Create a cluster environment with xgbost_ray in the anyscale console.
 * Create a Ray cluster in Anyscale.

**NOTE**: 

The data set is huge, so running locally on your laptop may not work for the 11GB dataset. 
Make sure that your Anyscale Ray cluster has access to the S3 bucket you uploaded your dataset. 

### Cluster Config:
 * 10 machines (m5.4xlarge), each with 16 cores and 64GB of memory, including the headnode.
