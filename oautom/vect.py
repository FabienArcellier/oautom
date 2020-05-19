import copy
from datetime import datetime
from typing import List

from oautom.execution.execution import Execution, ExecutionState


class Vect:
    """
    an instance of execution
    """

    def __init__(self, name: str, executions: List[Execution]):
        executions = copy.deepcopy(executions)
        self._name = name
        self._executions = executions
        self._start_date = datetime.now()
        for execution in self._executions:
            execution.initialize()

    def run_if_ready(self):
        for execution in self._executions:
            execution.run_if_ready()
            execution.check_if_done()

    def ended(self) -> bool:
        ended = True
        for execution in self._executions:
            ended &= execution.status() == ExecutionState.done

        return ended

    def status(self) -> dict:
        status = dict()
        status['name'] = self._name
        status['ended'] = self.ended()
        status['start_date'] = self._start_date.isoformat()
        status['executions'] = []
        for execution in self._executions:
            status['executions'].append((execution.name(), execution.status()))

        return status
