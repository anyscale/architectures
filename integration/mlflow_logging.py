import mlflow
import mlflow.sklearn

import logging

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)

with mlflow.start_run():
    alpha = "ALPHA"
    l1_ratio = "L1"
    rmse = "RMSE"
    r2 = "R2"
    mae = "MAE"
    mlflow.log_param("alpha", alpha)
    mlflow.log_param("l1_ratio", l1_ratio)
    mlflow.log_metric("rmse", rmse)
    mlflow.log_metric("r2", r2)
    mlflow.log_metric("mae", mae)