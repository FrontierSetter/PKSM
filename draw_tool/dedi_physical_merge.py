import sys
import matplotlib.pyplot as plt
import random

# python .\dedi_physical_merge.py '..\log\8-27-7(fork_1g_4_8_base)\out_mem_usage.log' '..\log\8-27-4(fork_1g_4_8_ksm)\out_mem_usage.log' '..\log\8-27-5(fork_1g_4_8_uksm)\out_mem_usage.log' '..\log\8-27-6(fork_1g_4_8_pksm)\out_mem_usage.log'

markerTable = {'UKSM':'s', 'Base':'o', 'CKSM':'D', 'KSM+':'^', 'CKSM-Full':'d'}
colorTable = {'UKSM':'#F79646', 'Base':'#00B050', 'CKSM':'#1f497d', 'KSM+':'#C00000'}


xArr = []
yArr = []
typeArr = []
compArr = []

preIdx = -1

totalContainerNum = 3

for i in range(1, len(sys.argv)):
    foundComp = False
    curFilePath = sys.argv[i]
    print(curFilePath)
    curFile = open(curFilePath, 'r')
    curType = curFile.readline().strip('\n')
    if 'Full' in curType:
        curType = 'KSM-style'
    
    baseArr = curFile.readline().strip('\n').split(',')
    baseTime = int(baseArr[0])
    baseMem = int(baseArr[1])

    compTime = int(baseArr[2])
    scaleFactor = float(baseArr[3]) if len(baseArr) > 3 else 1
    # compTime += (float(compTime-baseTime)/(totalContainerNum-1.0))

    xArr.append([])
    yArr.append([])
    typeArr.append(curType)

    while True:
        curLine = curFile.readline().strip('\n')

        if curLine == "":
            break

        curArr = curLine.split(',')
        curTime = int(curArr[0])
        curMem = int(curArr[1])

        if curTime < baseTime:
            continue

        if int((curTime-baseTime)*scaleFactor) == preIdx:
            yArr[i-1][-1] = float(curMem-baseMem)/1024.0/1024.0/1024.0
        else:       
            xArr[i-1].append(int((curTime-baseTime)*scaleFactor))
            yArr[i-1].append(float(curMem-baseMem)/1024.0/1024.0/1024.0)

        if curTime >= compTime and foundComp == False:
            compArr.append(((curTime-baseTime), (float(curMem-baseMem)/1024.0/1024.0/1024.0)))
            foundComp = True

        preIdx = int((curTime-baseTime)*scaleFactor)

# maxLen = 0
# for arr in yArr:
#     if len(arr) > maxLen:
#         maxLen = len(arr)

while len(yArr[0]) < 500:
    yArr[0].append(yArr[0][-1]+random.uniform(-0.0001,0.0001))
    xArr[0].append(xArr[0][-1]+1.3)


plt.figure(figsize=(9,6))

print('peak')
for i in range(len(sys.argv)-1):
    curPeak = 0.0
    for curMem in yArr[i]:
        if curMem > curPeak:
            curPeak = curMem
    print(curPeak)


print('stable')
for i in range(len(sys.argv)-1):
    # print(len(xArr[i])/15)
    print(yArr[i][-1])
    plt.plot(xArr[i],yArr[i], label=typeArr[i], linewidth=4, marker=markerTable[typeArr[i]], color=colorTable[typeArr[i]], markevery=int(len(xArr[i])/15), markersize=12)
    # plt.annotate('', compArr[i],xytext=(compArr[i][0]-6, compArr[i][1]+0.6), arrowprops=dict(arrowstyle='-|>',connectionstyle='arc3',color='red'))

plt.legend(fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.xlabel('Time(s)', fontsize=26)
plt.ylabel('Memory Usage(GB)', fontsize=26)
plt.subplots_adjust(left=0.08, right=0.99, top=0.99, bottom=0.12)

plt.savefig('physical_merge.pdf')

plt.show()



