import os
import sys

camps=[]
objects = os.listdir(os.path.join('.','scenarios'))
for item in objects:
    if item.endswith('.py') and not item.startswith('__'):
        scen=item.rstrip('.py')
        try:
            exec ("from scenarios.%s import Desc"%(scen))
            exec ("camps.append(%s.Desc)"%(scen))
        except :
           print ("There's a problem with %s"%(scen))
           print (sys.exc_info())
           sys.exit()
