import os

from celery import Celery
from kombu.common import Broadcast

rabbit_host = "guest:guest@localhost:5672"

if 'RABBITMQ_HOST' in os.environ:
    rabbit_host = os.environ['RABBITMQ_HOST']


class CeleryConf:
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_IMPORTS = ()
    CELERY_QUEUES = (Broadcast('agent_broadcast_tasks'),)


def create_app(imports):
    app = Celery('test_agent', broker='pyamqp://{}//'.format(rabbit_host))
    config = CeleryConf()
    import_list = list(config.CELERY_IMPORTS)
    for i in imports:
        import_list.append(i)
    config.CELERY_IMPORTS = tuple(import_list)
    app.config_from_object(config)
    return app
