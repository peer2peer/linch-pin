#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Samvaran Kashyap Rallabandi -  <srallaba@redhat.com>
#
# output parser  for Ansible based infra provsioning tooli, linch-pin
DOCUMENTATION = '''
---
version_added: "0.1"
module: topo_check
short_description: output_parser module in ansible
description:
  - This module allows a user to parser the output yaml file and register it as variable in ansible.

options:
  output_file:
    description:
      path to topology output file can be in json/yaml format
    required: true

author: Samvaran Kashyap Rallabandi -
'''

from ansible.module_utils.basic import *
import datetime
import sys
import json
import os
import shlex
import tempfile
import yaml
import jsonschema
from jsonschema import validate


def check_file_paths(module, *args):
    for file_path in args:
        if not os.path.exists(file_path):
            module.fail_json(msg= "File not found %s not found" % (file_path))
        if not os.access(file_path, os.R_OK):
            module.fail_json(msg= "File not accesible %s not found" % (file_path))
        if os.path.isdir(file_path):
            module.fail_json(msg= "Recursive directory not supported  %s " % (file_path))

def main():
    module = AnsibleModule(
    argument_spec={
            'output_file':     {'required': True, 'aliases': ['topology_output_file']},
        },
        required_one_of=[],
        supports_check_mode=True
    )
    data_file_path = os.path.expanduser(module.params['output_file'])
    check_file_paths(module, data_file_path)
    content = open(data_file_path,"r").read()
    c = yaml.load(content)
    resp = {"path": data_file_path, "content":c}
    if resp["content"]:
         changed = True
         module.exit_json(changed=changed, output=resp)
    else:
         module.fail_json(msg=resp)

from ansible.module_utils.basic import *
main()
