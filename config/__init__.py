# -*- coding: utf-8 -*-

import yaml
import os

def get_config():
    config_file_name = './conf.yaml'
    config_file_path = os.path.abspath(os.path.join(config_file_name))

    if not os.path.exists(config_file_path):
        raise FileExistsError('config not found.')
    with open(config_file_path) as f:
        return yaml.load(f)

if __name__=='__main__':
    print(get_config())