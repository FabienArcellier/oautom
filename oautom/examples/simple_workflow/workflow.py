from execution.bash_execution import BashExecution
from oautom import OAutom, OAutomMode, Flow

oautom = OAutom(mode=OAutomMode.foreground)

flow = Flow('flow 1', app=oautom)
step1 = BashExecution('execution 1', flow=flow, command='echo test')
step2 = BashExecution('sleep', flow=flow, command='sleep 60')
step3 = BashExecution('execution 2', flow=flow, command='echo test2')
step2.depends(step1)
step3.depends(step2)

oautom.plan('flow 1', minutes=1)
oautom.run()


