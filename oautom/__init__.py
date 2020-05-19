import json
from enum import Enum
from functools import partial
from typing import Dict

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.base import BaseScheduler
from apscheduler.schedulers.blocking import BlockingScheduler

from flow import Flow
from logger import get_logger
from vect import Vect
from vect_already_running_exception import VectAlreadyRunningException


class OAutomMode(Enum):
    foreground = 'foreground'
    background = 'background'


class OAutom:

    def __init__(self, mode: OAutomMode = OAutomMode.foreground):
        self._logger = get_logger()
        self._flows = {}  # type: Dict[str, Flow]
        self._running_vects = {}  # type: Dict[str, Vect]
        self._vects_history = []  # type: List[Vect]
        self._scheduler = self._event_loop(mode)

    def flows(self):
        return [flow.name() for flow in self._flows.values()]

    def logs(self):
        return [vect.status() for vect in self._vects_history]

    def register_flow(self, flow: 'Flow'):
        self._flows[flow.name()] = flow

    def run(self):
        self._scheduler.start()

    def start(self, flow_name: str):
        """

        :raise VectAlreadyRunningException
        :param flow_name:
        :return:
        """
        if self._vect_not_running(flow_name):
            vect = self._flows[flow_name].vect()
            self._running_vects[flow_name] = vect
            self._vects_history.insert(0, vect)
            self._logger.info(f"run a new vect for {flow_name}")
        else:
            raise VectAlreadyRunningException()

    def plan(self, flow_name: str, days: int = 0, hours: int = 0, minutes: int = 0):
        start_with_flow_name = partial(self.start, flow_name)
        self._scheduler.add_job(start_with_flow_name,
                                trigger="interval",
                                days=days,
                                hours=hours,
                                minutes=minutes)

    def status(self, flow_name: str):
        status_ = {}
        if flow_name in self._running_vects:
            status_ = self._running_vects[flow_name].status()

        return status_

    def _event_loop(self, mode: OAutomMode) -> BaseScheduler:
        if mode == OAutomMode.background:
            scheduler = BackgroundScheduler()
        elif mode == OAutomMode.foreground:
            scheduler = BlockingScheduler()
        else:
            raise ValueError(f'invalid mode {mode}')

        self._job = scheduler.add_job(func=self._move_vects_if_ready,
                                      trigger="interval",
                                      seconds=10)
        return scheduler

    def _move_vects_if_ready(self):
        for vect in self._running_vects.values():
            vect.run_if_ready()

    def _vect_not_running(self, flow_name):
        return flow_name not in self._running_vects or \
               self._running_vects[flow_name].ended()
