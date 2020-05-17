# pylint: disable=useless-super-delegation
import json
from concurrent.futures import ThreadPoolExecutor, Future

import boto3

from oautom import get_logger
from oautom.execution.execution import Execution


class LambdaExecution(Execution):

    def __init__(self, name: str, flow: 'Flow', lambda_function: str, payload: dict = {}):
        super().__init__(name, flow)
        self._future = None  # type: Future
        self._lambda_arn = lambda_function
        self._payload = payload

    def run(self):
        super().run()
        # self._logger.info(f"lambda: {self._lambda_arn}")
        with ThreadPoolExecutor(max_workers=1) as executor:
            self._future = executor.submit(_run_lambda, self._lambda_arn, self._payload)

    def check(self) -> bool:
        return self._future.done()


def _run_lambda(lambda_function: str, payload: dict):
    logger = get_logger()
    logger.info(f"lambda: {lambda_function}")
    client = boto3.client('lambda')
    client.invoke(
        FunctionName=lambda_function,
        InvocationType='RequestResponse',
        LogType='None',
        Payload=json.dumps(payload),
    )
