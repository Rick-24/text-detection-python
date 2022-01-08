from docx import Document
from ltp import LTP

def file_read(filePath):
    document_input = Document(filePath)
    all_paragraphs = document_input.paragraphs
    segment_num = 0
    sentence_list = []
    for paragraph in all_paragraphs:
        sentences = paragraph.text
        if sentences != "":  # 舍弃空句
            segment_num += 1
            sentences = sentences.split("。")
            for sentence_num, text in enumerate(sentences):
                if text != "":
                    sentence_list.append({'text': text, 'segment_num': segment_num, 'sentence_num': sentence_num + 1})

    return sentence_list