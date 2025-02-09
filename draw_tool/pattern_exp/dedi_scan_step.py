import sys
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

# python .\dedi_scan_step.py '..\log\7-30-10(nginx32_layer)\out_scan_step_cnt.log' 
# python .\dedi_scan_step.py '..\log\7-30-11(elastic16_layer)\out_scan_step_cnt.log'

inputFile = open(sys.argv[1], 'r')

baseArr = inputFile.readline().strip('\n').split(',')
baseTime = int(baseArr[0])
scaleTimeFactor = float(baseArr[1]) if len(baseArr) > 1 else 1.0
scaleMemFactor = float(baseArr[2]) if len(baseArr) > 1 else 1.0

timeArr = []
firstScan = []
nextScan = []

while True:
    curLine = inputFile.readline()
    
    if curLine == '':
        break

    curTime = int(curLine)

    if curTime < baseTime:
        inputFile.readline()
        inputFile.readline()
        continue

    curArr = [int(x) for x in inputFile.readline().strip('\n').split(' ') if x]
    inputFile.readline()

    # print(curArr)

    curFirst = 0
    curNext = 0

    for i in range(4):
        # print(curArr[i])
        curNext += curArr[i]

    for i in range(1):
        curFirst += curArr[-1-i]

    curStamp = int((curTime-baseTime)*scaleTimeFactor)
    if curStamp in timeArr:
        continue

    timeArr.append(curStamp)
    firstScan.append(curFirst*4.0/1024.0/1024.0*scaleMemFactor)
    nextScan.append(curNext*4.0/1024.0/1024.0*scaleMemFactor)

width = 0.8

plt.figure(figsize=(9,6))

legendEntryArr = ['First scan', 'Next scans']
legendArr = [
    plt.bar(timeArr, firstScan, width, color='#2a9d8f'),
    plt.bar(timeArr, nextScan, width, bottom=firstScan, color='#f4a261')
]
plt.legend(legendArr, legendEntryArr, fontsize=14)

# xfmt = ScalarFormatter(useMathText=True)
# xfmt.set_powerlimits((0, 0))
# plt.gca().yaxis.set_major_formatter(xfmt)
plt.xlim(0,timeArr[-1]+5)
plt.ylabel('Memory Merged(GB)', fontsize=18)
plt.xlabel('Time(s)', fontsize=18)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.subplots_adjust(left=0.08, right=0.99, top=0.96, bottom=0.11)

plt.savefig('scan_step.pdf')

plt.show()
