import os
import uuid

from celery import Celery
from kombu.common import Broadcast

rabbit_host = "guest:guest@localhost:5672"

if 'RABBITMQ_HOST' in os.environ:
    rabbit_host = os.environ['RABBITMQ_HOST']


class CeleryConf:
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_IMPORTS = ()
    CELERY_QUEUES = (Broadcast('agent_broadcast_tasks'),)


app = Celery('test_agent', broker='pyamqp://{}//'.format(rabbit_host))

app.config_from_object(CeleryConf())

# app.conf.task_queues = (Broadcast('agent_broadcast_tasks'),)
#
# app.conf.task_routes = {
#     'test_agent.start_session': {
#         'queue': 'agent_broadcast_tasks',
#         'exchange': 'agent_broadcast_tasks'
#     }
# }


@app.task(name='test_agent.start_session', queue="agent_broadcast_tasks")
def start_agent_session(_):
    pass


session_id = uuid.uuid4().hex
request = {'SUT_URL': 'test'}

# app.send_task('test_agent.start_session', exchange='custom_exchange', args=[request])
start_agent_session.delay(request)

