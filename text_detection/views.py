import json
import threading
import time
from concurrent import futures
from concurrent.futures.thread import ThreadPoolExecutor

import gensim
from django.http import JsonResponse
from py2neo import Graph

from text_detection.algorithm.keyWordDetect import key_word_detect
from text_detection.algorithm.process import document_analysis
from text_detection.neo4j.file_detect import detect
from text_detection.neo4j.file_insert import insert

print('Initializing Start...')
time_start = time.time()
model = gensim.models.Word2Vec.load('./text_detection/model/wiki.zh.text.model')
print(model.get_latest_training_loss())
time_end = time.time()
print('Initializing time cost = %fs' % (time_end - time_start))
print(model)


def textDetection(request):
    json_result = json.loads(request.body)
    print(json_result)

    filePath = json_result.get("filePath")

    sysRuleMap = json_result.get("sysRuleMap")
    province = sysRuleMap.get("PROVINCE")
    executor = ThreadPoolExecutor(max_workers=3)
    future_list = []
    for key, value in sysRuleMap.items():
        future = executor.submit(thread_process, filePath, value, key)
        future_list.append(future)
    result = {}
    for future in futures.as_completed(future_list):
        res = future.result()
        for key in res:
            result[key] = res[key]

    print(result)
    return JsonResponse(result, safe=False)


def thread_process(filePath_input, filePath_rules, key):
    match_list_total = []
    result = {}
    for filePath_rule in filePath_rules:
        print('Current Thread is %s 待匹配文件: %s ; 规则文件: %s' % (
            threading.current_thread().name, filePath_input, filePath_rule))
        match_list = document_analysis(filePath_input, filePath_rule, 0.9, 3)  ######调用两个文档的分析函数######
        match_list_total.append(match_list)
    result[key] = match_list_total
    return result


def file_insert(request):
    json_result = json.loads(request.body)
    filePath = json_result.get("filePath")
    type = json_result.get("type")
    fileName = json_result.get("fileName")
    print(filePath)
    print(fileName)
    print(type)
    g = Graph('http://localhost:7474', user='neo4j', password='123')
    info = {'filePath': filePath, 'fileName': fileName, 'type': type}
    insert(g, info)
    return JsonResponse("ok", safe=False)


def muti_file_insert(request):
    json_result = json.loads(request.body)
    sysRuleMap = json_result.get("sysRuleMap")
    g = Graph('http://localhost:7474', user='neo4j', password='123')
    for key, value in sysRuleMap.items():
        for file in value:
            fileName = file[file.rfind('/') + 1:]
            info = {'filePath': file, 'fileName': fileName, 'type': key}
            print(info)
            insert(g, info)
    return JsonResponse("ok", safe=False)


def file_detect(request):
    json_result = json.loads(request.body)
    file_path = json_result.get("filePath")
    g = Graph('http://localhost:7474', user='neo4j', password='123')
    result = detect(file_path, g)
    return JsonResponse(result, safe=False)


def key_detect(request):
    json_result = json.loads(request.body)
    file_path = json_result.get("filePath")
    keyWords = json_result.get("keywords")
    print(keyWords)
    key_words_spec = key_word_detect(file_path, keyWords)
    result = {'keyWords': key_words_spec}
    return JsonResponse(result, safe=False)
