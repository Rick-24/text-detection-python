import json
import threading
import time
from concurrent import futures
from concurrent.futures.thread import ThreadPoolExecutor

import gensim
from django.http import JsonResponse

from text_detection.algorithm.process import document_analysis

print('Initializing Start...')
time_start = time.time()
model = gensim.models.Word2Vec.load('F:/GitRepos/text-detection-python/text_detection/model/wiki.zh.text.model')
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
