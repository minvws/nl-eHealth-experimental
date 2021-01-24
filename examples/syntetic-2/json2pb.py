#!/usr/bin/python

import os, sys, json
from pprint import pprint
import protobuf_json
import json
import sys
import os
import glob
import urllib
import urllib2
import binascii
import inspect
import zlib
import time
import traceback

import msg_pb2 as pb_test

with open(sys.argv[1], 'r') as f:
  _j= f.read()
  f.close()

  json_obj=json.loads(_j)
  pb2=protobuf_json.json2pb(pb_test.MSG(), json_obj)

  pprint(pb2.SerializeToString())
