# Just an example of code which will overwrite output

import sys
import time

for i in range(10):
	sys.stdout.write("\r" + "loading" + "."*i)
	time.sleep(1)
	sys.stdout.flush()
print()
