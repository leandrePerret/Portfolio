from Experimentation import Experimentation
from Step import Step
import time
test = Experimentation()
test.setEtuve("192.168.1.73",502)
test.appendStep(Step(until=20,temperature=90))
test.appendStep(Step(until=20,temperature=45))
test.appendStep(Step(until=20,temperature=130))
test.launchExperimentation()
test.exportData()
test.execution = False