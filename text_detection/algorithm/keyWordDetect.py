from ltp import LTP

from text_detection.integration.docx import file_read


def key_word_detect(filePath, keyWords):
    sentence_list = file_read(filePath)
    ltp = LTP(path='./text_detection/model/base2.tgz')
    detect_result = []
    for sentence in sentence_list:
        for word in keyWords:
            if word in sentence['text']:
                detect_result.append(
                    {'segment_num': sentence['segment_num'], 'sentence_num': sentence['sentence_num'], 'word': word,
                     'text': sentence['text']})
    return detect_result
