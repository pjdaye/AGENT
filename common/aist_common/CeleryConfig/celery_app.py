import json
import os
from celery import Celery

redis_host = "localhost:32768"

if 'REDIS_HOST' in os.environ:
    redis_host = os.environ['REDIS_HOST']

# Support for PCF.
if 'VCAP_SERVICES' in os.environ:
    vcap_data = json.loads(os.environ['VCAP_SERVICES'])
    redis_cred = vcap_data['p-redis'][0]['credentials']
    redis_host = ":{}@{}:{}".format(redis_cred['password'], redis_cred['host'], redis_cred['port'])

app = Celery('test_agent', broker='redis://{}/0'.format(redis_host))