#!/usr/bin/env python

#pyyaml-6.0

import yaml

with open("/Users/george/dev/cogitogroupltd/boilerplate/task-clone.yaml", "r") as stream:
    try:
        task=yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

for i in task['spec']['params']:
  print(i['name'])
  # print(i['type'])
  # print(i['name'])
  # print(task['spec']['params']['description'])
  # print(task['spec']['params']['type'])
  # print(task['spec']['params']['default'])


  # print(i['name']+"|"+i['type']+"|"+i['default'])