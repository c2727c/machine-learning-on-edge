import test.test_1
import threading


threading.Thread(target=test.test_1.start).start()

import time

print('hi')
while (True):
	time.sleep(3)
	print(test.test_1.number)