# 加载模型

import jieba
import jieba.analyse as analyse
import numpy as np
from scipy.linalg import norm


# 使用word2vec对两个句子的相似度进行分析


def vector_similarity(s1, s2):
    from text_detection.views import model
    def sentence_vector(s):
        words = jieba.lcut(s)
        v = np.zeros(model.vector_size)  # 注意要与model的vector的size保持一直，否则无法进行array的计算
        for word in words:
            try:
                v += model.wv[word]
            except:
                pass
        v /= len(words)
        return v

    v1, v2 = sentence_vector(s1), sentence_vector(s2)
    return np.dot(v1, v2) / (norm(v1) * norm(v2))


# 使用jieba关键字对两个句子的相似度进行分析
def sentences_keyword_match(s1, s2):
    tr_result1 = analyse.textrank(s1, topK=10)  # 分析关键字
    tr_result2 = analyse.textrank(s2, topK=10)  # 分析关键字
    count = 0
    for keyword1 in tr_result1:
        for keyword2 in tr_result2:
            if keyword1 == keyword2:
                count += 1
    return count


def multithreading_simulate():  # 测试函数，不停调用document_analysis()分析函数，没用多线程
    import os
    from text_detection.algorithm.process import document_analysis
    input_folder = "D:/全部资料/研究生学前学习/政策NLP demo/rule/"
    fileName_input = "/input/检测文件-甘井子区经济工作奖励暂行办法.docx"
    filePath_input = input_folder + fileName_input

    rule_folder = 'D:/全部资料/研究生学前学习/政策NLP demo/rule/21/02/'
    fileName_rule = []
    for i in os.walk(rule_folder):
        if len(i[1]) != 0:  # 不包含子文件夹
            fileName_rule.extend(i[2])

    print(fileName_rule)
    match_list_total = []

    for f_name in fileName_rule:
        filePath_rule = rule_folder + f_name
        match_list = document_analysis(filePath_input, filePath_rule, 0.9, 3)  ######调用两个文档的分析函数######
        match_list_total.append(match_list)

    return match_list_total
