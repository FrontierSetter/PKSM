import sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import PercentFormatter

# colorDict = {
#     'waiting candidate': '#2a9d8f', 
#     'pattern record': '#e9c46a', 
#     'reverse map': '#f4a261'
# }

# colorDict = {
#     'waiting candidate': '#247ba0', 
#     'pattern record': '#f25f5c', 
#     'reverse map': '#43aa8b'
# }

colorDict = {
    'waiting candidate': '#247ba0', 
    'pattern record': '#ffe066', 
    'reverse map': '#f25f5c'
}

hatchDict = {
    'waiting candidate': '//', 
    'pattern record': '\\\\', 
    'reverse map': 'x'
}

markerTable = {'UKSM':'s', 'Base':'o', 'CKSM':'D', 'KSM+':'^', 'CKSM-Full':'d'}
colorTable = {'UKSM':'tab:orange', 'Base':'tab:blue', 'CKSM':'tab:green', 'KSM+':'tab:olive', 'CKSM-Full':'tab:pink'}


stageNameArr = ['waiting candidate', 'pattern record', 'reverse map']
tickArr = ['8','16','32','64','128']
dataScale = float(1024*1024*1024)    # B->GB
memoryScale = float(1024*1024*1024)       # GB->B

oriData = [
    {
        'name': '8',
        'memory': 8,
        'cksm': {
            # 'waiting candidate': 80*430178,
            # 'pattern record': 40*872643,
            # 'reverse map': 40*872643
            'waiting candidate': 80*423473,
            'pattern record': 40*170828,
            'reverse map': 40*686833
        },
        'uksm': {
            # 'waiting candidate': 192*460152,             # uksm_vma_slot
            # 'pattern record': 64*234496+72*31752,  # uksm_tree_node uksm_stable_node
            # 'reverse map': 80*217617+40*22848     # uksm_rmap_item uksm_node_vma
            'waiting candidate': 192*445094,             # uksm_vma_slot
            'pattern record': 64*97921+72*481,  # uksm_tree_node uksm_stable_node
            'reverse map': 80*222903+40*11822     # uksm_rmap_item uksm_node_vma

        },
        'ksm': {
            'waiting candidate': 48*12986,             # mm_slot
            'pattern record': 64*4105999,  # rmap_item
            'reverse map': 64*11095     # stable_node

        },
    },
    {
        'name': '16',
        'memory': 16,
        'cksm': {
            # 'waiting candidate': 80*833572,
            # 'pattern record': 40*1722168,
            # 'reverse map': 40*1722168
            'waiting candidate': 80*831437,
            'pattern record': 40*385427,
            'reverse map': 40*1355715
        },
        'uksm': {
            # 'waiting candidate': 192*898926,            
            # 'pattern record': 64*458559+72*50512, 
            # 'reverse map': 80*409530+40*21318 
            'waiting candidate': 192*876667,             # uksm_vma_slot
            'pattern record': 64*390189+72*958,  # uksm_tree_node uksm_stable_node
            'reverse map': 80*419403+40*10191     # uksm_rmap_item uksm_node_vma

        },
        'ksm': {
            'waiting candidate': 48*27713,             # mm_slot
            'pattern record': 64*8584478,  # rmap_item
            'reverse map': 64*18685     # stable_node

        },
    },
    {
        'name': '32',
        'memory': 32,
        'cksm': {
            # 'waiting candidate': 80*1979004,
            # 'pattern record': 40*3214254,
            # 'reverse map': 40*3214254
            'waiting candidate': 80*1930780,
            'pattern record': 40*639799,
            'reverse map': 40*2731564
        },
        'uksm': {
            # 'waiting candidate': 192*1779224,            
            # 'pattern record': 64*184256+72*88312,  926991
            # 'reverse map': 80*928098+40*26826 
            'waiting candidate': 192*1739741,             # uksm_vma_slot
            'pattern record': 64*926991+72*1129,  # uksm_tree_node uksm_stable_node
            'reverse map': 80*976478+40*18095     # uksm_rmap_item uksm_node_vma
        },
        'ksm': {
            'waiting candidate': 48*56208,             # mm_slot
            'pattern record': 64*18513971,  # rmap_item
            'reverse map': 64*33649     # stable_node

        },
    },
    {
        'name': '64',
        'memory': 64,
        'cksm': {
            # 'waiting candidate': 80*4285106,
            # 'pattern record': 40*6735468,
            # 'reverse map': 40*6735774
            'waiting candidate': 80*4038004,
            'pattern record': 40*1512379,
            'reverse map': 40*5400176
        },
        'uksm': {
            # 'waiting candidate': 192*3537261,            
            # 'pattern record': 64*2124992+72*164192, 
            # 'reverse map': 80*1917753+40*28254 
            'waiting candidate': 192*3465016,             # uksm_vma_slot
            'pattern record': 64*1828425+72*2625,  # uksm_tree_node uksm_stable_node
            'reverse map': 80*1917047+40*21929     # uksm_rmap_item uksm_node_vma

        },
        'ksm': {
            'waiting candidate': 48*113462,             # mm_slot
            'pattern record': 64*36923022,  # rmap_item
            'reverse map': 64*62096     # stable_node

        },
    },
    {
        'name': '128',
        'memory': 128,
        'cksm': {
            # 'waiting candidate': 80*8320752,
            # 'pattern record': 40*12754488,
            # 'reverse map': 40*12754590
            'waiting candidate': 80*8809826,
            'pattern record': 40*2970230,
            'reverse map': 40*10021571
        },
        'uksm': {
            # 'waiting candidate': 192*7046615,            
            # 'pattern record': 64*1001280+72*312704, 
            # 'reverse map': 80*2483853+40*42344 
            'waiting candidate': 192*6912191,             # uksm_vma_slot
            'pattern record': 64*2124992+72*4909,  # uksm_tree_node uksm_stable_node
            'reverse map': 80*3775968+40*30765     # uksm_rmap_item uksm_node_vma

        },
        'ksm': {
            'waiting candidate': 48*229960,             # mm_slot
            'pattern record': 64*72002012,  # rmap_item
            'reverse map': 64*120704     # stable_node

        },
    }
]

print(oriData)

# 获取柱状图数据
cksmArr = []
uksmArr = []
ksmArr = []

for stageName in stageNameArr:
    cksmArr.append([])
    uksmArr.append([])
    ksmArr.append([])
    for dataDict in oriData:
        curCKSM = dataDict['cksm'][stageName]/dataScale
        curUKSM = dataDict['uksm'][stageName]/dataScale
        curKSM = dataDict['ksm'][stageName]/dataScale
        cksmArr[-1].append(curCKSM)
        uksmArr[-1].append(curUKSM)
        ksmArr[-1].append(curKSM)
print(cksmArr)
print(uksmArr)
print(ksmArr)

# 获取折线图数据
cksmPercentArr = []
uksmPercentArr = []
ksmPercentArr = []

for dataDict in oriData:
    curCksmTotal = 0
    curUksmTotal = 0
    curKsmTotal = 0
    curMemory = dataDict['memory']*memoryScale
    for stageName in stageNameArr:
        curCksmTotal += dataDict['cksm'][stageName]
        curUksmTotal += dataDict['uksm'][stageName]
        curKsmTotal += dataDict['ksm'][stageName]
    cksmPercentArr.append(curCksmTotal/curMemory*100)
    uksmPercentArr.append(curUksmTotal/curMemory*100)
    ksmPercentArr.append(curKsmTotal/curMemory*100)
print(cksmPercentArr)
print(uksmPercentArr)
print(ksmPercentArr)


x=np.arange(len(tickArr))
width = 0.2
gap = 0.08*width

fig = plt.figure(figsize=(9,6))
plt.yticks(fontsize=20)
axBar = fig.add_subplot(111)
axPlot=axBar.twinx()

axPlot.plot(x-width-gap*1.5,ksmPercentArr, label='KSM+', linewidth=4, marker=markerTable['KSM+'], color=colorTable['KSM+'], markersize=9)
axPlot.plot(x,uksmPercentArr, label='UKSM', linewidth=4, marker=markerTable['UKSM'], color=colorTable['UKSM'], markersize=9)
axPlot.plot(x+width+gap*1.5,cksmPercentArr, label='CKSM', linewidth=4, marker=markerTable['CKSM'], color=colorTable['CKSM'], markersize=9)
# axPlot.set_ylim(0.5, 1.5)
axPlot.set_ylabel('Meta Data / Total Memory(%)', fontsize=26)
axPlot.legend(fontsize=22, loc='center right')


legendArrBar = []
legendEntryArrBar = []

baseArr = [0]*len(ksmArr[0])

for curStageArr,curEntry in zip(ksmArr,stageNameArr):
    curP = axBar.bar(x-width-gap*1.5, curStageArr, width, bottom=baseArr, color=colorDict[curEntry], hatch=hatchDict[curEntry],edgecolor='black', linewidth=1)

    for i in range(len(curStageArr)):
        baseArr[i] += curStageArr[i]

print('ksm all')
print(baseArr)

baseArr = [0]*len(uksmArr[0])

for curStageArr,curEntry in zip(uksmArr,stageNameArr):
    curP = axBar.bar(x, curStageArr, width, bottom=baseArr, color=colorDict[curEntry], hatch=hatchDict[curEntry],edgecolor='black', linewidth=1)

    for i in range(len(curStageArr)):
        baseArr[i] += curStageArr[i]

print('uksm all')
print(baseArr)

baseArr = [0]*len(cksmArr[0])

for curStageArr,curEntry in zip(cksmArr,stageNameArr):
    curP = axBar.bar(x+width+gap*1.5, curStageArr, width, bottom=baseArr, color=colorDict[curEntry], hatch=hatchDict[curEntry],edgecolor='black', linewidth=1)
    legendArrBar.insert(0,curP)
    legendEntryArrBar.insert(0,curEntry)

    for i in range(len(curStageArr)):
        baseArr[i] += curStageArr[i]

print('cksm all')
print(baseArr)



axBar.set_ylabel('Meta Data Usage(GB)', fontsize=26)
axBar.legend(legendArrBar, legendEntryArrBar, fontsize=22, loc='center left')
axBar.set_xticks(x)
axBar.set_xticklabels(tickArr, fontsize=20)
axBar.set_xlabel('Main Memory Capacity(GB)', fontsize=26)

plt.subplots_adjust(left=0.075, right=0.9, top=0.99, bottom=0.13)
plt.yticks(fontsize=20)

plt.savefig('scal_meta_stage_bar.pdf')
plt.show()