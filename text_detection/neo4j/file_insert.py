# -*- coding: utf-8 -*-
from docx import Document
from ltp import LTP
from py2neo import Graph, Node, Relationship, NodeMatcher, Subgraph

from text_detection.algorithm.ltp import semantic_analysis
from text_detection.integration.docx import file_read


def insert(graph, info):
    sentence_list = file_read(info['filePath'])
    ltp = LTP(path='G:/Downloads/base2.tgz')
    for sentence in sentence_list:
        temp = "".join([sentence['text']])
        info['segment_num'] = sentence['segment_num']
        info['sentence_num'] = sentence['sentence_num']
        info['text'] = temp
        result = semantic_analysis(ltp, temp)
        print(result)
        neo4j_insert_sentence(graph, result, info)


def neo4j_insert_sentence(graph, result, info):
    matcher = NodeMatcher(graph)
    file_node = matcher.match("File", name=info['fileName']).first()
    if not file_node:
        print("不存在")
        file_node = Node("File", name=info['fileName'], path=info['filePath'], type=info['type'])

    for relation in result:

        root_node = Node("Root", value=relation[-1][1], segment_num=info['segment_num'], sentence_num=info['sentence_num'],
                         text=info['text'])

        root_rela = Relationship(file_node, "Include", root_node)
        print(file_node)

        node_ls = [file_node, root_node]
        relation_ls = [root_rela]

        for rela in relation[:-1]:
            temp_node = Node("Text", value=rela[1])
            node_ls.append(temp_node)
            relation_ls.append(Relationship(root_node, rela[0], temp_node))
        subgraph = Subgraph(node_ls, relation_ls)
        tx = graph.begin()
        tx.create(subgraph)
        graph.commit(tx)


if __name__ == '__main__':
    info = {}
    text = "为贯彻落实《国务院关于促进创业投资持续健康发展的若干意见》（国发〔2016〕53号）精神，汇集推动大众创业、万众创新的重要资本力量，促进科技创新成果转化，落实新发展理念、实施创新驱动发展战略、推进供给侧结构性改革、培育发展新动能和稳增长、扩就业，实现技术、资本、人才、管理等创新要素与创业企业有效结合的投融资方式，为全省经济社会发展注入新动力，打造新引擎，现制定以下政策措施"
    info['filePath'] = "F:/GitRepos/text-detection/"
    info['fileName'] = "test"
    info['segment_num'] = 1
    info['sentence_num'] = 1
    info['text'] = text
    info['type'] = "province"

    result = semantic_analysis(text)
    g = Graph('http://localhost:7474', user='neo4j', password='123')
    neo4j_insert_sentence(g, result, info)
