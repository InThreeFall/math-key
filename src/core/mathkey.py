from pynput import keyboard
from core.ime import IME
import core.loader as loader

def getValueByStateStr():
    return MathKeyController.state.split(':')

def getLatterBykey(key): 
    inKey = key
    for i in loader.load_keyList():
        if key == keyboard.KeyCode.from_char(i):
            inKey = i
            break
    return inKey
def isLatter(key):
    print(key)
    if key in loader.load_keyList():
        return True
    return False
def mapKey2Str(key):
    if key == keyboard.Key.space:
        inKey = 'space'
    #如果输入的是回车
    elif key == keyboard.Key.enter:
        inKey = 'enter'
    #如果是左箭头和右箭头和上箭头和下箭头
    elif key == keyboard.Key.left:
        inKey = 'left'
    elif key == keyboard.Key.right:
        inKey = 'right'
    elif key == keyboard.Key.up:
        inKey = 'up'
    elif key == keyboard.Key.down:
        inKey = 'down'
    #如果是ese
    elif key == keyboard.Key.esc:
        inKey = 'esc'
    #如果是退格键
    elif key == keyboard.Key.backspace:
        inKey = 'backspace'
    else:
        inKey = key
    return inKey
def on_press(key):
    try:
        print(MathKeyController.inputKey)
        fun,state = getValueByStateStr()
        if state == 'off':
            return
        inKey = getLatterBykey(key)#如果输入的是字母,则获取对应的字母
        inKey = mapKey2Str(inKey)
        if fun=='输入法' and MathKeyController.state in MathKeyController.corpusNamelist:
            typeInput = state
            pinyinStateSwitch(inKey,typeInput)
        elif fun=='映射' and MathKeyController.state in MathKeyController.mappinglist:
            typeInput = state
            getAndType(inKey,typeInput)
    except AttributeError as e:
        print(e)

def getAndType(key,typeInput):
    #检测是否是字母
    if not isLatter(key):
        return
    control = keyboard.Controller()#从map.json获取对应的按键映射
    try:
        key_str = loader.getValueByKey(typeInput,key)           
        control.press(keyboard.Key.backspace)
        control.type(key_str)
    except Exception as e:
        print(e)

def reset():
    MathKeyController.candidate = []
    MathKeyController.selected = 0
    MathKeyController.inputKey = ''
    MathKeyController.showCandidate = []
    MathKeyController.showCandidatePage = 0

deleteNum = 0
writeNum = 0
def deleteN(num):
    control = keyboard.Controller()
    for i in range(num):
        control.press(keyboard.Key.backspace)
        control.release(keyboard.Key.backspace)
def pinyinStateSwitch(key,typeInput):
    control = keyboard.Controller()
    #如果输入的是回车
    global deleteNum,writeNum
    if key == 'enter':
        deleteNum = len(MathKeyController.inputKey)+1
        #一次性打印deleteNum个退格键
        deleteN(deleteNum)
        if len(MathKeyController.candidate) > 0:
            print(typeInput)
            if typeInput == 'Latex':
                #在config中获取candidate对应的latex
                latexStr = loader.getLatexStrByValue(MathKeyController.candidate[MathKeyController.selected])
                if latexStr == None:
                    writeNum = len("暂无对应的latex")
                    control.type("暂无对应的latex")
                else:
                    writeNum = len(latexStr)-1
                    control.type(latexStr)
                reset()
                return
            control.type(MathKeyController.candidate[MathKeyController.selected])
        reset()
        return
    #如果输入的是空格
    if key == 'space':
        if len(MathKeyController.inputKey)==0:
            return
        reset()
        #输入一个退格键
        deleteN(1)
        return
    #如果输入的是下箭头
    if key == 'up':
        if MathKeyController.selected > 0:
            MathKeyController.selected -= 1
            if MathKeyController.selected < MathKeyController.showCandidatePage*5:
                MathKeyController.showCandidatePage -= 1
                MathKeyController.showCandidate = MathKeyController.candidate[MathKeyController.showCandidatePage*5:MathKeyController.showCandidatePage*5+5]
        return
    #如果输入的是上箭头
    if key == 'down':
        if MathKeyController.selected < len(MathKeyController.candidate) - 1:
            MathKeyController.selected += 1
            if MathKeyController.selected > MathKeyController.showCandidatePage*5+4:
                MathKeyController.showCandidatePage += 1
                MathKeyController.showCandidate = MathKeyController.candidate[MathKeyController.showCandidatePage*5:MathKeyController.showCandidatePage*5+5]
        return
    #如果输入的是上箭头
    # if key == 'up':
    #     if MathKeyController.showCandidatePage > 0:
    #         MathKeyController.showCandidatePage -= 1
    #     MathKeyController.showCandidate = MathKeyController.candidate[MathKeyController.showCandidatePage*5:MathKeyController.showCandidatePage*5+5]
    #     #选中的候选词
    #     MathKeyController.selected = MathKeyController.showCandidatePage*5
    #     return
    # #如果输入的是下箭头
    # if key == 'down':
    #     if MathKeyController.showCandidatePage < len(MathKeyController.candidate) // 5:
    #         MathKeyController.showCandidatePage += 1
    #     MathKeyController.showCandidate = MathKeyController.candidate[MathKeyController.showCandidatePage*5:MathKeyController.showCandidatePage*5+5]
    #     MathKeyController.selected = MathKeyController.showCandidatePage*5
    #     return
    #如果输入的是esc键
    if key == 'esc':
        reset()
        return
    #如果输入的是退格键
    if key == 'backspace':
        if deleteNum > 0:
            deleteNum -= 1
            return
        if len(MathKeyController.inputKey) > 0:
            MathKeyController.inputKey = MathKeyController.inputKey[:-1]
        #获取候选词
        if len(MathKeyController.inputKey) > 0:
            scores = IME().getScoresByX(MathKeyController.inputKey,typeInput)
            MathKeyController.candidate = [i[1] for i in scores]
            #取前5个候选词
            MathKeyController.showCandidate = MathKeyController.candidate[:5]
            MathKeyController.showCandidatePage = 0
            MathKeyController.selected = 0
        else:
            reset()
        return
    if not isLatter(key):
        return
    if writeNum > 0:
        writeNum -= 1
        return
    #如果输入的是字母
    MathKeyController.inputKey += key
    #获取候选词
    if len(MathKeyController.inputKey) > 0:
        scores = IME().getScoresByX(MathKeyController.inputKey,typeInput)
        MathKeyController.candidate = [i[1] for i in scores]
        #取前5个候选词
        MathKeyController.showCandidate = MathKeyController.candidate[:5]
        MathKeyController.showCandidatePage = 0
        MathKeyController.selected = 0
    else:
        MathKeyController.candidate = []
        MathKeyController.selected = 0

def on_release(key):
    pass
     
def on_change(cmd = None):
    if cmd != None:
        MathKeyController.state = cmd
    else:
        MathKeyController.state = MathKeyController.stateList[(MathKeyController.stateList.index(MathKeyController.state) + 1) % len(MathKeyController.stateList)]        

class MathKeyController:

    @staticmethod
    def on_change_state(cmd = None):
        on_change(cmd)

    @staticmethod
    def listenerStart():
        MathKeyController.listener.start()
    
    @staticmethod
    def listenerStop():
        MathKeyController.listener.stop()

    @staticmethod
    def globalStart():
        MathKeyController.globalListener.start()

    @staticmethod
    def globalStop():
        MathKeyController.globalListener.stop()

    #从文件中读取快捷键
    changeStateHotKey = loader.load_config('changeState')

    #创建映射列表
    mappinglist = loader.load_mappingNameList()
    mappinglist = list(map(lambda x:"映射:"+x,mappinglist))
    configlist = loader.load_configNameList()
    configlist = list(map(lambda x:"配置:"+x,configlist))
    corpusNamelist = loader.load_corpusNameList()
    corpusNamelist = list(map(lambda x:"输入法:"+x,corpusNamelist))
    stateList = mappinglist + corpusNamelist
    stateList.append('状态:off')
    state = stateList[0]
    #候选词
    candidate = []
    #选中的候选词
    showCandidate = []
    showCandidatePage = 0
    selected = 0
    inputKey = ''

    listener = keyboard.Listener(on_press=on_press,on_release=on_release)
    globalListener = keyboard.GlobalHotKeys({
        changeStateHotKey: on_change})
