from flow import Flow


class OAutom:

    def __init__(self, mode: str):
        self._mode = mode
        self._flows = {}

    def start(self, flow_name: str):
        pass

    def register_flow(self, flow: 'Flow'):
        self._flows[flow.name()] = flow

    def refresh_schedule(minutes: int):
        pass
