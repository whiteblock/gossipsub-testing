import re
import matplotlib.pyplot as plt

ORCHESTRA_LOGFILE = 'node96'

pattern = re.compile('(?:Orchestra publish request sent: )(?:\d+)(?:, )(?P<time>\d+)')

f = open(ORCHESTRA_LOGFILE, "r")

lines = f.readlines()

nanotimes = []
diff_times = []

cnt = 0
for line in lines:
    cnt+=1
    match = pattern.search(line)
    if match != None:
        nanotimes.append(int(match.group('time')))


f.close()

for x, y in zip(nanotimes[0::], nanotimes[1::]):
    print
    diff_times.append((y-x) * 1E-6)


fig = plt.plot(diff_times)

plt.show()



