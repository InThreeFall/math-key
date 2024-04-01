"""
数据加载器
"""
import json
from config import STATIC

"""
加载语料库名称列表
"""
def load_corpusNameList():
    file = open(STATIC.CORPUS_PATH, 'r',encoding='utf-8')
    js = json.load(file)
    #获取js所有的key
    corpusNameList = list(js.keys())
    return corpusNameList

def load_corpus(corpusName):
    file = open(STATIC.CORPUS_PATH, 'r',encoding='utf-8')
    js = json.load(file)
    corpus = js[corpusName]
    return corpus


"""
加载映射名称列表
"""
def load_mappingNameList():
    file = open(STATIC.MAP_PATH, 'r',encoding='utf-8')
    js = json.load(file)
    mappingNameList = list(js.keys())
    return mappingNameList

def load_mapping(mappingName):
    file = open(STATIC.MAP_PATH, 'r',encoding='utf-8')
    js = json.load(file)
    mapping = js[mappingName]
    return mapping
def getValueByKey(mappingName,key):
    file = open(STATIC.MAP_PATH, 'r',encoding='utf-8')
    js = json.load(file)
    mapping = js[mappingName]
    return mapping[key]

"""
加载配置名称列表
"""
def load_configNameList():
    file = open(STATIC.CONFIG_PATH, 'r',encoding='utf-8')
    js = json.load(file)
    configNameList = list(js.keys())
    return configNameList

def load_config(configName):
    file = open(STATIC.CONFIG_PATH, 'r',encoding='utf-8')
    js = json.load(file)
    config = js[configName]
    return config


"""
键符
"""
def load_keyList():
    return ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
            'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',]