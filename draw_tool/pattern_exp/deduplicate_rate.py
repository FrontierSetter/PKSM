import sys
import os.path

# 输出两列数据，用逗号分隔：时间戳，当时内存使用情况Byte
# 第一行为数据备注
# 第二行为基本参数：起始时间戳，内存基准
# 第一二行的信息需要人工填写

inputFilePath = sys.argv[1]
pathTuple = os.path.split(inputFilePath)
print(pathTuple)

inputFile = open(inputFilePath, 'r')
outputFile = open(os.path.join(pathTuple[0], 'out_'+pathTuple[1]), 'w')

inputFile.readline()

maxMem = 0
stableMem = 0

baseFile = open(sys.argv[2], 'r')
baseFile.readline()
baseTime = int(baseFile.readline())
baseFile.close()

getBase = False
baseTime = 0
baseMem = 0

while True:
    curLine = inputFile.readline().strip('\n')
    if curLine == "":
        break

    curTime = int(curLine)
    inputFile.readline()
    curLineArr = [x for x in inputFile.readline().strip('\n').split(' ') if x]
    curMem = int(curLineArr[2])
    inputFile.readline()

    outputFile.write("%d,%d\n" % (curTime, curMem))

    if curTime < baseTime:
        continue

    if not getBase:
        baseMem = curMem
        getBase = True
    
    curMem -= baseMem

    if curMem > maxMem:
        maxMem = curMem
    
    stableMem = curMem

outputFile.close()
inputFile.close()

print("max: %d\tstable: %d" % (maxMem, stableMem))