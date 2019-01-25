import threading
import time
import uuid

import celery.worker
from aist_common.CeleryConfig.celery_app import create_app
from aist_common.log import get_logger

LOGGER = get_logger('agent-explore-and-test')

LOGGER.info("Starting agent...")

app = create_app(['inbound_tasks', 'outbound_tasks'])

worker = celery.worker.WorkController(app=app,
                                      hostname="test-agent-" + uuid.uuid4().hex,
                                      pool_cls='solo',
                                      queues=['test_agent_queue', 'agent_broadcast_tasks'])

threading.Thread(target=worker.start).start()

LOGGER.info("Celery started.")
LOGGER.info("Agent started.")
