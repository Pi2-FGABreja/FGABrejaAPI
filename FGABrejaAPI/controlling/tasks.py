from __future__ import absolute_import
from controlling.stages.controll import StageControll
from celery.decorators import task
import logging

logger = logging.getLogger('fga-breja')


@task(name="controll_process")
def controll_process():
    logger.info("[StageControll] Task triggered!")
    StageControll.handle_states()
