from controlling.stages import (pre_brewery, brewery, filtering,
                                boiling, cooling, fermentation)
from controlling.models import Process
from django.core.exceptions import ObjectDoesNotExist
import logging

logger = logging.getLogger('fga-breja')


class StageControll(object):

    @classmethod
    def handle_states(cls):
        try:
            process = Process.current()
        except ObjectDoesNotExist:
            logger.info("[StageControll] Any process started.")
            return

        if process.state in pre_brewery.STATES.values():
            controll = pre_brewery.PreBreweryControll(process)
            controll.handle_states()
        elif process.state in brewery.STATES.values():
            controll = brewery.BreweryControll(process)
            controll.handle_states()
        elif process.state in filtering.STATES.values():
            controll = filtering.FilteringControll(process)
            controll.handle_states()
        elif process.state in boiling.STATES.values():
            controll = boiling.BoilingControll(process)
            controll.handle_states()
        elif process.state in cooling.STATES.values():
            controll = cooling.CoolingControll(process)
            controll.handle_states()
        elif process.state in fermentation.STATES.values():
            controll = fermentation.FermentationControll(process)
            controll.handle_states()
