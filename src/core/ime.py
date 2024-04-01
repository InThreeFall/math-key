import config.STATIC as STATIC
import json
class IME:
    def __init__(self,file_path = STATIC.CORPUS_PATH):
        self.file_path = file_path
        with open(self.file_path, 'r',encoding='utf-8') as f:
            self.corpus = json.load(f)

    def __weight_input_string(X):
        """为输入字符串X加权。"""
        Fx = [10 - i for i in range(len(X))]
        return Fx

    def __calculate_score(Fx, aliases, X):
        """根据别名列表计算得分。"""
        max_score = 0
        for A in aliases:
            FA = [10 - i for i in range(len(A))]
            Pxa = IME.__find_matches(X, A)
            score = 0
            for (i, j) in Pxa:
                if i != 0:
                    score += Fx[i - 1] * FA[j - 1]  # i和j是从1开始的索引，所以需要减1
                else:
                    score += 0
            max_score = max(max_score, score)  # 取所有别名中的最高得分
        return max_score

    def __find_matches(X, A):
        """在A中找到X的匹配，并记录位置。"""
        Pxa = []
        for x in X:
            if x in A:
                i = X.index(x) + 1  # 在X中的索引，加1是为了匹配算法描述中的非零开始
                j = A.index(x) + 1  # 在A中的索引，加1同上
                Pxa.append((i, j))
            else:
                Pxa.append((0, 0))  # 如果A中没有X的字符，记录为(0, 0)
        return Pxa

    def __sort_corpus(X, corpus):
        Fx = IME.__weight_input_string(X)
        scores = []
        for key, aliases in corpus.items():
            score = IME.__calculate_score(Fx, aliases, X)
            if score > 0:  # 只有得分大于0的项才被考虑
                scores.append((score, key))

        # 根据得分排序
        scores.sort(reverse=True)
        
        return scores

    def getScoresByX(self,X,lang):
        # 从语言库中获取别名列表
        corpus = self.corpus[lang]
        scores = IME.__sort_corpus(X, corpus)
        return scores
    
