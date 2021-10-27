
from anyscale import AnyscaleSDK
import os
import json

sdk = AnyscaleSDK(os.environ["ANYSCALE_CLI_TOKEN"])

def save_cluster_environment(id):
    response = sdk.get_cluster_environment_build(id)
    env_config = response.result.config_json.to_dict()
    with open(f'{id}.json', 'w') as f:
       json.dump(env_config, f)


save_cluster_environment("bld_cxezEkgtJq2WC4XdhKiUruvL")
id ="bld_cxezEkgtJq2WC4XdhKiUruvL"



