import os
os.chdir('C:\\Users\\JackWong\\Downloads\\p\\pig_ops\\webroot\\testing')

from ztest_simul import *


t = TestSimul(1)
t.test_simul_sow('Diday')

t = TestSimul(1)
t.run()