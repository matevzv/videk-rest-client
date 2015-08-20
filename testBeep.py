from beep import Beep

nodeName = "1401003"

beep = Beep(nodeName)

v = beep.getBatteryVoltage()
s = beep.getSignalStrength()
w = beep.getWeight()

print str(v)
print str(s)
print str(w)
