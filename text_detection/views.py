from django.http import HttpResponse, JsonResponse
import json

from text_detection.algorithm.jieba import document_analysis


def textDetection(request):
    json_result = json.loads(request.body)
    filePath = json_result.get("filePath")
    match_list = document_analysis(filePath)
    return JsonResponse(match_list, safe=False)

