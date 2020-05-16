from oautom.execution.execution import Execution


class LambdaExecution(Execution):

    def __init__(self, name: str, flow: 'Flow'):
        super().__init__(name, flow)
