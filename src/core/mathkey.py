from pynput import keyboard
import json
import config.STATIC as STATIC
def on_press(key):
    try:
        #如果输入的是 小写a
        if MathKeyController.state == 'off':
            return
        inKey = ''
        #字母表：a-z 大小写
        dirABC = ['a','b','c','d','e','f','g','h','i','j',
                  'k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'
                  'A','B','C','D','E','F','G','H','I','J',
                  'K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        #遍历字母表，如果输入的是字母表中的字母
        for i in dirABC:
            if key == keyboard.KeyCode.from_char(i):
                inKey = i
                break
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
    hotKey = js['hotkey']

    file = open(STATIC.MAP_PATH, 'r',encoding='utf-8')
    js = json.load(file)
    #获取js所有的key
    stateList = list(js.keys())
    stateList.append('off')
    state = stateList[0]
    
    listener = keyboard.Listener(on_press=on_press,on_release=on_release)
    globalListener = keyboard.GlobalHotKeys({
        hotKey: on_change})
