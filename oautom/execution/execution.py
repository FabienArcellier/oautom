class Execution:

    def __init__(self, name: str, flow: 'Flow'):
        self._name = name
        flow.register_execution(self)
        self._depends = []

    def depends(self, previous: 'Execution'):
        self._depends.append(previous)

