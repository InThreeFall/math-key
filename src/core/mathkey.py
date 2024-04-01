from pynput import keyboard
import json
import config.STATIC as STATIC
from core.ime import IME

def on_press(key):
    try:
        inKey = ''
        dirABC = ['a','b','c','d','e','f','g','h','i','j',
                  'k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'
                  'A','B','C','D','E','F','G','H','I','J',
                  'K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        if MathKeyController.state == 'off':
            return
        #如果输入的是字母,则获取对应的字母
        for i in dirABC:
            if key == keyboard.KeyCode.from_char(i):
                inKey = i
                break
        #如果输入的是空格
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
        if MathKeyController.state == 'pinyin':
            pinyinStateSwitch(inKey,keyboard.Controller())
        else:
            getAndType(inKey,keyboard.Controller())
    except AttributeError:
        pass

def getAndType(key,control):
    control = keyboard.Controller()
    #从map.json获取对应的按键
    try:
        with open(STATIC.MAP_PATH, 'r',encoding='utf-8') as f:
            map = json.load(f)
            #从map对象中获取MathKeyController.state对应的映射对象
            map = map[MathKeyController.state]
            key_str = map[key]
            #按下删除键
            control.press(keyboard.Key.backspace)
            control.type(key_str)
    except Exception as e:
        pass

deleteNum = 0
def pinyinStateSwitch(key,control):
    print("输入：",MathKeyController.inputKey)
    #如果输入的是回车
    global deleteNum
    print("deleteNum:",deleteNum)
    if key == 'enter':
        deleteNum = len(MathKeyController.inputKey)+1
        #一次性打印deleteNum个退格键
        for i in range(deleteNum):
            control.press(keyboard.Key.backspace)
            control.release(keyboard.Key.backspace)
        control.type(MathKeyController.candidate[MathKeyController.selected])
        MathKeyController.candidate = []
        MathKeyController.selected = 0
        MathKeyController.inputKey = ''
        MathKeyController.showCandidate = []
        MathKeyController.showCandidatePage = 0
        return
    #如果输入的是空格
    if key == 'space':
        MathKeyController.candidate = []
        MathKeyController.selected = 0
        MathKeyController.inputKey = ''
        MathKeyController.showCandidate = []
        MathKeyController.showCandidatePage = 0
        #输入一个退格键
        control.press(keyboard.Key.backspace)
        control.release(keyboard.Key.backspace)
        return
    #如果输入的是左箭头
    if key == 'left':
        if MathKeyController.selected > 0:
            MathKeyController.selected -= 1
            if MathKeyController.selected < MathKeyController.showCandidatePage*5:
                MathKeyController.showCandidatePage -= 1
                MathKeyController.showCandidate = MathKeyController.candidate[MathKeyController.showCandidatePage*5:MathKeyController.showCandidatePage*5+5]
        return
    #如果输入的是右箭头
    if key == 'right':
        if MathKeyController.selected < len(MathKeyController.candidate) - 1:
            MathKeyController.selected += 1
            if MathKeyController.selected > MathKeyController.showCandidatePage*5+4:
                MathKeyController.showCandidatePage += 1
                MathKeyController.showCandidate = MathKeyController.candidate[MathKeyController.showCandidatePage*5:MathKeyController.showCandidatePage*5+5]
        return
    #如果输入的是上箭头
    if key == 'up':
        if MathKeyController.showCandidatePage > 0:
            MathKeyController.showCandidatePage -= 1
        MathKeyController.showCandidate = MathKeyController.candidate[MathKeyController.showCandidatePage*5:MathKeyController.showCandidatePage*5+5]
        #选中的候选词
        MathKeyController.selected = MathKeyController.showCandidatePage*5
        return
    #如果输入的是下箭头
    if key == 'down':
        if MathKeyController.showCandidatePage < len(MathKeyController.candidate) // 5:
            MathKeyController.showCandidatePage += 1
        MathKeyController.showCandidate = MathKeyController.candidate[MathKeyController.showCandidatePage*5:MathKeyController.showCandidatePage*5+5]
        MathKeyController.selected = MathKeyController.showCandidatePage*5
        return
    #如果输入的是esc键
    if key == 'esc':
        MathKeyController.candidate = []
        MathKeyController.selected = 0
        MathKeyController.inputKey = ''
        MathKeyController.showCandidate = []
        MathKeyController.showCandidatePage = 0
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
            scores = IME().getScoresByX(MathKeyController.inputKey,"希腊")
            MathKeyController.candidate = [i[1] for i in scores]
            #取前5个候选词
            MathKeyController.showCandidate = MathKeyController.candidate[:5]
            MathKeyController.showCandidatePage = 0
            MathKeyController.selected = 0
        else:
            MathKeyController.showCandidatePage = 0
            MathKeyController.showCandidate = []
            MathKeyController.candidate = []
            MathKeyController.selected = 0
        return
    if not checkIsLetter(key):
        return
    #如果输入的是字母
    MathKeyController.inputKey += key
    #获取候选词
    if len(MathKeyController.inputKey) > 0:
        scores = IME().getScoresByX(MathKeyController.inputKey,"希腊")
        MathKeyController.candidate = [i[1] for i in scores]
        #取前5个候选词
        MathKeyController.showCandidate = MathKeyController.candidate[:5]
        MathKeyController.showCandidatePage = 0
        MathKeyController.selected = 0
    else:
        MathKeyController.candidate = []
        MathKeyController.selected = 0


def checkIsLetter(key):
    dirABC = ['a','b','c','d','e','f','g','h','i','j',
              'k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'
              'A','B','C','D','E','F','G','H','I','J',
              'K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    for i in dirABC:
        if key == i:
            return True
    return False


def on_release(key):
    if key == keyboard.Key.esc:
        # 释放了esc 键，停止监听
        return False
     
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
    file = open(STATIC.CONFIG_PATH, 'r',encoding='utf-8')
    js = json.load(file)
    changeStateHotKey = js['changeState']

    file = open(STATIC.MAP_PATH, 'r',encoding='utf-8')
    js = json.load(file)
    #获取js所有的key
    stateList = list(js.keys())
    stateList.append('off')
    stateList.append('pinyin')
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
